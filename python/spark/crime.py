from datetime import datetime
from functools import partial
import operator


from numpy import array

from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, ArrayType, IntegerType, StringType

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.evaluation import MulticlassMetrics

from pyspark.mllib.clustering import KMeans

##########################
# This is supposed to demonstrate some proficiency with spark and using ML algorithms
# It's in 1 file to make it easier to peruse
##########################



print("Chicago Crime")
spark = SparkSession.builder.appName("ChicagoCrime").getOrCreate()
df = spark.read.format("csv").option("header","true").load("data/crimes.csv")
df.createOrReplaceTempView("crime")

sql = """
  select
    (select count(*) from crime where Domestic="true") as domestic_count,
    (select count(*) from crime where Arrest="true") as arrest_count,
    count(*) as total_crimes
    from crime
"""
# show that we can do SQL
spark.sql(sql).show()

# Spark UDFs to deal with conversions
def dt_converter(str_date):
  return datetime.strptime(str_date, "%m/%d/%Y %I:%M:%S %p")

def contains_str(col, search):
  count = 0
  for w in col.split(" "):
    if w == search:
      count = count + 1
  return count

def word_freq(word_list, col):
  col = col.lower()
  freqs = []
  for w in word_list:
    freqs.append(contains_str(col, w.lower()))
  return freqs

# Let's do some feature engineering
# We can use word frequency for the most common words in the crime description
# Say BATTERY shows up 3 times, that helps categorize the crime.

key_words = [ "SIMPLE",
              "DOMESTIC",
              "BATTERY",
              "POSS",
              "UNDER",
              "THEFT",
              "VEHICLE",
              "PROPERTY",
              "CANNABIS",
              "LESS",
              "HANDGUN",
              "ENTRY",
              "AGGRAVATED",
              "AUTOMOBILE",
              "FROM",
              "BUILDING",
              "RETAIL",
              "WEAPON",
              "FINANCIAL",
              "UNLAWFUL",
              "FORCIBLE",
              "IDENTITY",
              "TELEPHONE",
              "LAND",
              "HARASSMENT",
              "FRAUD",
              "HEROIN(WHITE)",
              "CARD",
              "VIOLATION",
              "THREAT"]

# register our UDFs
spark.udf.register("dt_convert", dt_converter, TimestampType())
spark.udf.register("word_freq", partial(word_freq, key_words) , ArrayType(IntegerType()))

##############################
# Supervised Learning
##############################

# This will act as our labels
# we can use the offset for the Primary Type as the label
primary_types = []
for t in spark.sql("Select distinct `Primary Type` as PrimaryType from crime").collect():
  primary_types.append(t.PrimaryType)

print("Primary Types ", len(primary_types), " types ", primary_types)
# use Spark SQL to generate feature set
feature_sql = """
  select
    `Primary Type` as PrimaryType,
    int(hour(dt_convert(Date)) / 8) as PartOfDay,
    word_freq(Description) as WordFreq,
    `Community Area` as Community,
    int(boolean(Domestic)) as Domestic,
    int(boolean(Arrest)) as Arrest
  from
    crime
"""

features = spark.sql(feature_sql)

training_labels = []
testing_labels = []

def append_label(labels, crime):
  feats = []
  feats.extend(crime.WordFreq)
  feats.append(crime.PartOfDay)
  feats.append(int(crime.Community))
  feats.append(crime.Domestic)
  feats.append(crime.Arrest)
  labels.append(LabeledPoint(primary_types.index(crime.PrimaryType), feats))

# create our training set
for crime in features.collect()[:8000]:
  append_label(training_labels, crime)

# create a testing set
for crime in features.collect()[8001:]:
  append_label(testing_labels, crime)

# multinomial crime type classifier
# We use part of day, word frequencies for common words, where it is, whether it was domestic, whether it was an arrest
model = LogisticRegressionWithLBFGS.train(spark.sparkContext.parallelize(training_labels), iterations=10, numClasses=len(primary_types))

# let's see how accurate we are
predictionAndLabels = [(float(model.predict(lp.features)), lp.label) for lp in testing_labels]
metrics = MulticlassMetrics(spark.sparkContext.parallelize(predictionAndLabels))
precision = metrics.precision()
recall = metrics.recall()
f1Score = metrics.fMeasure()
accuracy = metrics.accuracy
print("Summary Stats")
print("Precision = %s" % precision)
print("Recall = %s" % recall)
print("F1 Score = %s" % f1Score)
print("Accuracy = %s" % accuracy) # this was about 81% accurate which is pretty good

############################################
# Unsupervised Learning, KMeans Clustering
############################################
kmeans_rows = []
def feat_array(crime):
  feats = []
  feats.extend(crime.WordFreq)
  feats.append(crime.PartOfDay)
  feats.append(int(crime.Community))
  feats.append(crime.Domestic)
  feats.append(crime.Arrest)
  return array(feats)

for crime in features.collect():
  kmeans_rows.append(feat_array(crime))

k = KMeans.train(spark.sparkContext.parallelize(kmeans_rows), 15)

clusters = {}
for p in primary_types:
  clusters[p] = {}

# It's not realistic to think clusters will line up with Primary Type
# But this illustrates a way to try to investigate how it clustered
for c in features.collect():
  feat = feat_array(c)
  clustered = k.predict(feat)
  if clustered in clusters[c.PrimaryType]:
    clusters[c.PrimaryType][clustered] = clusters[c.PrimaryType][clustered] + 1
  else:
    clusters[c.PrimaryType][clustered] = 1

print("Clusters ", clusters["BATTERY"])

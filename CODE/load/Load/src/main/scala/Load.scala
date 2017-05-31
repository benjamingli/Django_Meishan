import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

import org.apache.spark.mllib.linalg._
import org.apache.spark.mllib.regression._

import org.apache.spark.mllib.tree.DecisionTree
import org.apache.spark.mllib.tree.model.DecisionTreeModel
import org.apache.spark.mllib.util.MLUtils


object SimpleApp {
  def main(args: Array[String]) {
    if(args.length != 4) {
      println("Usage: *.jar <countInt> <input> <input.date> <output>")
      return
    }
    val count : Int = args(0).toInt
    val rawFile = args(1)
    val preFile = args(2)
    val outFile = args(3)

    val conf = new SparkConf().setAppName("Load")
    val sc = new SparkContext(conf)
    val rawData = sc.textFile(rawFile)
    val preData = sc.textFile(preFile)

    val raw = rawData.map { line =>
      val values = line.split(',').map(_.toDouble)
      val featureVector = Vectors.dense(values.init)
      val label = values.last
      LabeledPoint(label, featureVector)
    }
    val pre = preData.map { line =>
      val values = line.split(',').map(_.toDouble)
      val featureVector = Vectors.dense(values.init)
      val label = values.last
      LabeledPoint(label, featureVector)
    }

    val model = DecisionTree.trainRegressor(
      raw, Map(0 -> count, 5 -> 2, 8 -> 5), "variance", 20, 150)

    val labelsAndPredictions = pre.map { point =>
      val prediction = model.predict(point.features)
      (point.label, prediction)
    }

    labelsAndPredictions.sortBy(_._1).map(t => "%05d,%.3f".format(t._1.toInt,t._2)).saveAsTextFile(outFile)
  }
}

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf


object SimpleApp {
  def main(args: Array[String]) {
    if(args.length!=2) {
      println("Usage: *.jar <input> <output>")
      return
    }
    val rawFile = args(0)
    val outFile = args(1)

    val conf = new SparkConf().setAppName("Yxbw")
    val sc = new SparkContext(conf)
    val rawData = sc.textFile(rawFile)
    val key = rawData.map(Trim.brk)
    val keyCount = key.map(word => (word,1)).reduceByKey(_ + _)
    keyCount.sortBy(_._2, false).map(t => "%s,%s".format(t._1,t._2)).saveAsTextFile(outFile)
  }
}

object Trim {
  def brk(s: String): String = {
    val RE = """.+\d{2}分\d{2}秒\s+(.+)\s+(合闸|分闸|遥信变位分|开关分位|开关合位).+""".r
    s match {
      case RE(name, other) => s"""$name"""
      case _ => s"[FAIL] $s"
    }
  }
}

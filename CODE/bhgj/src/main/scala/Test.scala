import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf


object SimpleApp {
  def main(args: Array[String]) {
    if(args.length!=4) {
      println("Usage: *.jar <input> <output> 10 50")
      return
    }
    val rawFile = args(0)
    val outFile = args(1)
    val hourThreshold : Int = args(2).toInt
    val dayThreshold : Int = args(3).toInt

    val conf = new SparkConf().setAppName("Bhgj")
    val sc = new SparkContext(conf)
    val rawData = sc.textFile(rawFile).filter(line => !(line.contains("复归")))
    val key = rawData.map(Trim.core).distinct
    val hourKey = key.map(Trim.hour).reduceByKey(_ + _)
    hourKey.cache()
    val dayKey = hourKey.map(Trim.day).reduceByKey(_ + _).filter(t => t._2 >= dayThreshold)
    val result = hourKey.filter(t => t._2 >= hourThreshold).union(dayKey).map(Trim.divid).map(Classification.warn)
    result.sortBy(_._1, false).map(t => "%s,%s,%s,%s".format(t._1,t._2,t._3,t._4)).saveAsTextFile(outFile)
  }
}

object Trim {
  def core(s: String): String = {
    val RE1 = """.+(\d{4}年.+\d{2}秒)\s+(.+--[1-6]).+""".r
    val RE2 = """.+(\d{4}年.+\d{2}秒)\s+(.+)\s+动作.+""".r
    s match {
      case RE1(time, name) => s"$time$name"
      case RE2(time, name) => s"$time$name"
      case _ => s"[FAIL] $s"
    }
  }
  def hour(s: String): (String, Int) = {
    val RE = """(.+)\d{2}分\d{2}秒(.+)""".r
    s match {
      case RE(time, name) => (s"""$time$name""", 1)
      case _ => (s"[FAIL] $s", 1)
    }
  }
  def day(s: (String, Int)): (String, Int) = {
    val RE = """(.+)\d{2}时(.+)""".r
    s._1 match {
      case RE(time, name) => (s"""$time$name""", s._2)
      case _ => (s"[FAIL]", s._2)
    }
  }
  def divid(s: (String, Int)): (String, String, Int) = {
    val RE1 = """(.+\d{2}时)(.+)""".r
    val RE2 = """(.+\d{2}日)(.+)""".r
    s._1 match {
      case RE1(time, name) => (time, name, s._2)
      case RE2(time, name) => (time, name, s._2)
      case _ => (s"[FAIL]", s._1, s._2)
    }
  }
}

object Classification {
  def warn(s: (String, String, Int)): (String, String, String, Int) = {
    val RE01 = """.+(SF6气压低闭锁|油压低.+闭锁|N2泄漏闭锁|空气压力低.+闭锁|储能电机故障|小电流接地告警|弹簧未储能).*""".r
    val RE02 = """.+(SF6气压低告警|油压低告警|N2泄漏告警|油泵打压超时|气泵打压超时|气泵.+告警|加热器故障|机构就地控制).*""".r
    val RE03 = """.+(控制回路断线|控制电源消失|保护重合闸闭锁|保护.+断线|保护.+失电|保护装置故障|保护通道异常|测控装置通信中断|机构就地控制|测控保护装置通信中断).*""".r
    val RE04 = """.+(保护远跳.+信|保护切换.+接通|保护装置异常|保护装置通信中断|测控装置异常).*""".r
    val RE07 = """.+(过流保护出口).*""".r
    val RE09 = """.+(冷却器电源消失|冷却器风扇故障|冷却器强迫油循环故障|冷却器全停告警|油温过高告警|母线接地).*""".r
    val RE10 = """.+(压力释放告警|压力突变告警|油温高告警|油位异常|有载轻瓦斯告警|有载压力释放告警|有载油位异常|过载闭锁有载调压).*""".r
    val RE11 = """.+(冷却器控制器故障).*""".r
    val RE12 = """.+(非电气量保护装置异常|保护过负荷告警).*""".r
    val RE13 = """.+(接地告警).*""".r
    val RE15 = """.+(TV.+跳开|母差.+告警).*""".r
    val RE16 = """.+(母差开入信号异常告警|保护开入.*异常).*""".r
    val RE19 = """.+(备自投装置故障|直流系统接地|直流电源系统交流输入故障).*""".r
    val RE20 = """.+(备自投出口|电源异常|备自投装置异常|直流母线电压异常|直流电源控制装置通信中断|直流系统异常).*""".r
    val RE23 = """.+(监控系统故障|监控逆变电源故障|消防装置故障告警).*""".r
    val RE24 = """.+(监控系统异常|远动装置异常|GPS.*异常|PMU.*异常|故障录波.*异常|监控逆变电源异常|其它公共设备异常|消防装置火灾告警|高压脉冲防盗告警|边界防盗告警).*""".r
    val RE27 = """.+(合并单元装置故障|智能终端装置故障).*""".r
    val RE28 = """.+(合并.+异常|智能终端.+异常|GOOSE|SV|就地控制|对时异常).*""".r
    s._2 match {
      case RE01(other) => (s._1, s._2, "一次故障", s._3)
      case RE02(other) => (s._1, s._2, "一次告警", s._3)
      case RE03(other) => (s._1, s._2, "二次故障", s._3)
      case RE04(other) => (s._1, s._2, "二次告警", s._3)
      case RE07(other) => (s._1, s._2, "二次故障", s._3)
      case RE09(other) => (s._1, s._2, "一次故障", s._3)
      case RE10(other) => (s._1, s._2, "一次告警", s._3)
      case RE11(other) => (s._1, s._2, "二次故障", s._3)
      case RE12(other) => (s._1, s._2, "二次告警", s._3)
      case RE13(other) => (s._1, s._2, "一次故障", s._3)
      case RE15(other) => (s._1, s._2, "二次故障", s._3)
      case RE16(other) => (s._1, s._2, "二次告警", s._3)
      case RE19(other) => (s._1, s._2, "二次故障", s._3)
      case RE20(other) => (s._1, s._2, "二次告警", s._3)
      case RE23(other) => (s._1, s._2, "二次故障", s._3)
      case RE24(other) => (s._1, s._2, "二次告警", s._3)
      case RE27(other) => (s._1, s._2, "二次故障", s._3)
      case RE28(other) => (s._1, s._2, "二次告警", s._3)
      case _ => (s._1, s._2, "", s._3)
    }
  }
}

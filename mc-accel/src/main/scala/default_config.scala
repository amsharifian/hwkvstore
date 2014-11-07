package McAccel

import Chisel._

class DefaultConfig extends ChiselConfig {
  private def isPowerOfTwo(num: Ex[Int], start: Int, end: Int) = {
    var expr: Ex[Boolean] = ExEq(num, ExLit(start))
    var check = 2 * start
    while (check <= end) {
      expr = ExOr(expr, ExEq(num, ExLit(check)))
      check = 2 * check
    }
    expr
  }
  override val topDefinitions:World.TopDefs = {
    (pname,site,here) => pname match {
      case "wordsize" => Knob("wordsize")
      case "keysize"  => 256
      case "numkeys"  => Knob("numkeys")
      case "valcachesize" => Knob("valcachesize")
      case "tagsize" => 16
    }
  }
  override val topConstraints:List[ViewSym=>Ex[Boolean]] = List(
    ex => isPowerOfTwo(ex[Int]("wordsize"), 8, 64),
    ex => isPowerOfTwo(ex[Int]("numkeys"), 256, 1024),
    ex => isPowerOfTwo(ex[Int]("valcachesize"), 1024, 1024 * 1024)
  )
  override val knobValues:Any=>Any = {
    case "wordsize" => 32
    case "numkeys" => 1024
    case "valcachesize" => 512 * 1024
  }
}

-- LuaTools需要PROJECT和VERSION这两个信息
PROJECT = "helloworld"
VERSION = "1.0.0"


local sys = require "sys"

log.info("main", "hello world")

print(_VERSION)

sys.timerLoopStart(function()
    print("hi, LuatOS")
end, 3000)




sys.run()


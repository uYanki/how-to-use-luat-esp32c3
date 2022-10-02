PROJECT = "memdemo"
VERSION = "1.0.0"

local sys = require "sys"

sys.taskInit(function()
    local count = 1
    while 1 do
        sys.wait(1000)
        log.info("luatos", rtos.meminfo())
        log.info("luatos", rtos.meminfo("sys"))
        count = count + 1
    end
end)




sys.run()


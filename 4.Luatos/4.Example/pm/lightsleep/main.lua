PROJECT = "pm"
VERSION = "1.0.0"


local sys = require "sys"

-- gpio唤醒
sys.taskInit(
    function()
        while 1 do
            log.info("lightsleep", "I want to sleep, press gpio9 to wake me up")
            esp32.enterLightSleep(esp32.GPIO, 9, 0)
            log.info("wakeup", "gpio9")
            sys.wait(1000) -- 硬核消抖？
        end
    end
)

-- rtc唤醒
-- sys.taskInit(
--     function()
--         while 1 do
--             log.info("lightsleep", "I want sleep 10s")
--             esp32.enterLightSleep(esp32.RTC, 10 * 1000 * 1000)
--             log.info("wakeup", "10s")
--         end
--     end
-- )



sys.run()


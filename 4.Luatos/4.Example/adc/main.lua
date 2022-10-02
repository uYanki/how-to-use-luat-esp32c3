PROJECT = "adcdemo"
VERSION = "1.0.0"


local sys = require "sys"

sys.taskInit(
    function()
        for i = 0, 4 do
            adc.open(i)
        end
        while 1 do
            for i = 0, 4 do
                log.info("adc" .. i, adc.read(i))
            end
            sys.wait(1000)
        end
    end
)



sys.run()


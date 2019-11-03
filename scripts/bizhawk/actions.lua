-- Action module
local M = {}

function M.process(action)

    defaultInput = {["Down"] = false,
                    ["Left"] = false,
                    ["Right"] = false,
                    ["Up"] = false,
                    ["B1"] = false,
                    ["B2"] = false}

    if action == 0 then -- RIGHT
        defaultInput["Right"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 1 then -- RIGHT + FIRE
        defaultInput["Right"] = true
        defaultInput["B1"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 2 then -- RIGHT + JUMP
        defaultInput["Right"] = true
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 3 then -- RIGHT + JUMP + FIRE
        defaultInput["Right"] = true
        defaultInput["B1"] = true
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end    
    
    if action == 4 then -- LEFT
        defaultInput["Left"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 5 then -- -- LEFT + FIRE
        defaultInput["Left"] = true
        defaultInput["B1"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 6 then -- -- LEFT + JUMP
        defaultInput["Left"] = true
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 7 then -- -- LEFT + FIRE + JUMP 
        defaultInput["Left"] = true
        defaultInput["B1"] = true
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 8 then -- FIRE
        defaultInput["B1"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 9 then -- JUMP
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end

    if action == 10 then -- FIRE + JUMP
        defaultInput["B1"] = true
        defaultInput["B2"] = true
        joypad.set(defaultInput, 1)
    end

end

return M
-- Memory module
local M = {}

function M.get_vitality()
    return memory.read_u8(0x0C36, "Main RAM")
end

return M
-- Memory module
local M = {}

function M.get_vitality()
    return memory.read_u8(0x0C36, "Main RAM")
end

function M.get_is_dead()
    return (memory.read_u8(0x0007, "Main RAM") + memory.read_u8(0x0008, "Main RAM")) == 0
end

function M.get_level_position()
    return (memory.read_u8(0x012C, "Main RAM") * 255) + memory.read_u8(0x012B, "Main RAM")
end

function M.get_score()
    return (memory.read_u8(0x0121, "Main RAM") * 10) + (memory.read_u8(0x0122, "Main RAM") * 1000) + (memory.read_u8(0x0123, "Main RAM") * 100000)
end

return M
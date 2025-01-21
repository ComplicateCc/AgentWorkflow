local FileHandler = {}
FileHandler.__index = FileHandler

-- 创建文件处理器实例
-- @param filename 文件名
-- @return 文件处理器实例
function FileHandler:new(filename)
    local obj = {}
    setmetatable(obj, FileHandler)
    obj.filename = filename
    return obj
end

-- 读取文件内容
-- @return 文件内容，如果文件不存在则返回nil
function FileHandler:read_file()
    local file = io.open(self.filename, "r")
    if file then
        local content = file:read("*all")
        file:close()
        return content
    else
        print("文件 " .. self.filename .. " 不存在。")
        return nil
    end
end

-- 写入内容到文件
-- @param content 要写入的内容
function FileHandler:write_file(content)
    local file = io.open(self.filename, "w")
    if file then
        file:write(content)
        file:close()
    else
        print("写入文件 " .. self.filename .. " 时出错。")
    end
end

-- 追加内容到文件
-- @param content 要追加的内容
function FileHandler:append_file(content)
    local file = io.open(self.filename, "a")
    if file then
        file:write(content)
        file:close()
    else
        print("追加文件 " .. self.filename .. " 时出错。")
    end
end

-- 获取文件大小
-- @return 文件大小（字节），如果文件不存在则返回0
function FileHandler:get_file_size()
    local file = io.open(self.filename, "r")
    if file then
        local current = file:seek()
        local size = file:seek("end")
        file:seek("set", current)
        file:close()
        return size
    else
        print("文件 " .. self.filename .. " 不存在。")
        return 0
    end
end

-- 读取用户输入
print("请输入内容：")
local user_input = io.read()

-- 创建文件处理器实例
local file_handler = FileHandler:new("output.txt")

-- 写入用户输入到文件
file_handler:write_file(user_input)

-- 读取文件内容
local file_content = file_handler:read_file()
if file_content then
    print("文件内容：" .. file_content)
end

-- 获取文件大小
local file_size = file_handler:get_file_size()
print("文件大小：" .. file_size .. " 字节")

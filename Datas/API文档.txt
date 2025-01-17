local FileHandler = {}
FileHandler.__index = FileHandler

function FileHandler:new(filename)
    local obj = {}
    setmetatable(obj, FileHandler)
    obj.filename = filename
    return obj
end

function FileHandler:read_file()
    local file = io.open(self.filename, "r")
    if file then
        local content = file:read("*all")
        file:close()
        return content
    else
        print("文件 ".. self.filename.." 不存在。")
        return nil
    end
end

function FileHandler:write_file(content)
    local file = io.open(self.filename, "w")
    if file then
        file:write(content)
        file:close()
    else
        print("写入文件 ".. self.filename.." 时出错。")
    end
end

function FileHandler:append_file(content)
    local file = io.open(self.filename, "a")
    if file then
        file:write(content)
        file:close()
    else
        print("追加文件 ".. self.filename.." 时出错。")
    end
end

function FileHandler:get_file_size()
    local file = io.open(self.filename, "r")
    if file then
        local current = file:seek()
        local size = file:seek("end")
        file:seek("set", current)
        file:close()
        return size
    else
        print("文件 ".. self.filename.." 不存在。")
        return 0
    end
end
local FileHandler = {}
FileHandler.__index = FileHandler

-- �����ļ�������ʵ��
-- @param filename �ļ���
-- @return �ļ�������ʵ��
function FileHandler:new(filename)
    local obj = {}
    setmetatable(obj, FileHandler)
    obj.filename = filename
    return obj
end

-- ��ȡ�ļ�����
-- @return �ļ����ݣ�����ļ��������򷵻�nil
function FileHandler:read_file()
    local file = io.open(self.filename, "r")
    if file then
        local content = file:read("*all")
        file:close()
        return content
    else
        print("�ļ� " .. self.filename .. " �����ڡ�")
        return nil
    end
end

-- д�����ݵ��ļ�
-- @param content Ҫд�������
function FileHandler:write_file(content)
    local file = io.open(self.filename, "w")
    if file then
        file:write(content)
        file:close()
    else
        print("д���ļ� " .. self.filename .. " ʱ����")
    end
end

-- ׷�����ݵ��ļ�
-- @param content Ҫ׷�ӵ�����
function FileHandler:append_file(content)
    local file = io.open(self.filename, "a")
    if file then
        file:write(content)
        file:close()
    else
        print("׷���ļ� " .. self.filename .. " ʱ����")
    end
end

-- ��ȡ�ļ���С
-- @return �ļ���С���ֽڣ�������ļ��������򷵻�0
function FileHandler:get_file_size()
    local file = io.open(self.filename, "r")
    if file then
        local current = file:seek()
        local size = file:seek("end")
        file:seek("set", current)
        file:close()
        return size
    else
        print("�ļ� " .. self.filename .. " �����ڡ�")
        return 0
    end
end

-- ��ȡ�û�����
print("���������ݣ�")
local user_input = io.read()

-- �����ļ�������ʵ��
local file_handler = FileHandler:new("output.txt")

-- д���û����뵽�ļ�
file_handler:write_file(user_input)

-- ��ȡ�ļ�����
local file_content = file_handler:read_file()
if file_content then
    print("�ļ����ݣ�" .. file_content)
end

-- ��ȡ�ļ���С
local file_size = file_handler:get_file_size()
print("�ļ���С��" .. file_size .. " �ֽ�")

% 类定义
classdef SQLite3 < handle
    % 属性
    properties(Hidden)
        % 数据库连接
        connection
    end
    % 方法
    methods
        % 初始化函数
        function object = SQLite3(fileName)
            % 建立连接
            object.connection = sqlite(fileName);
            % 检查结果
            if object.connection.IsOpen == 1
                % 打印信息
                fprintf("SQLite3.SQLite3 : database opened !\n");
            else
                % 打印信息
                fprintf("SQLite3.SQLite3 : failed to open database !\n");
            end
        end

        % 是否开启
        function value = IsOpened(object)
            % 返回结果
            value = object.connection.IsOpen;
        end

        % 关闭连接
        function Close(object)
            % 检查连接
            if object.IsOpened()
                % 关闭连接
                close(object.connection)
                % 打印信息
                fprintf("SQLite3.Close : database closed !\n");
            else
                % 打印信息
                fprintf("SQLite3.Close : database already closed !\n");
            end
        end

        % 获得计数
        function frequency = GetFrequency(object, word)
            % 检查参数
            assert(object.IsOpened())
            % 执行查询操作
            results = fetch(object.connection, ...
                "SELECT count FROM words WHERE content = '" + word + "'", MaxRows = 1);
            % 获得数据
            if isempty(results.count)
                % 设置返回值
                frequency = 0.0;
            else
                % 设置返回值
                frequency = results.count(1);
            end
        end
    end
end
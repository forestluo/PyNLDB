% 类定义
classdef TokenVector < handle
    % 属性
    properties(Constant)
        N = 4;
    end
    properties
        % 字符
        token
        % 计数
        count
        % 矢量
        vector
    end
    properties(Hidden)
        % 备份值
        backup
    end
    % 方法
    methods
        % 初始化函数
        function object = TokenVector(token, count)
            % 检查参数
            assert(strlength(token) == 1)
            %{
            % 检查参数
            if strlength(token) > 1
                % 打印信息
                fprintf("TokenVector.TokenVector : token(%s).length = %d !\n", token, strlength(token))
            end
            %}
            % 设置计数器
            object.count = count;
            % 设置参数
            object.token = token;
            % 设置随机矢量
            object.vector = rand(1, TokenVector.N);
            % 设置备份值
            object.backup = object.vector;
        end

        % 重置
        function Reset(object)
            % 设置随机矢量
            object.vector = rand(1, TokenVector.N);
            % 设置备份值
            object.backup = object.vector;
        end

        % 备份当前矢量
        function Backup(object)
            % 备份当前矢量
            object.backup = object.vector;
        end

        % 当前值与备份值距离
        function error = Error(object)
            % 返回结果
            error = pdist2(object.vector, object.backup);
        end

        % 当前矢量分量值不能过小
        function result = NoSmallValue(object)
            % 返回结果
            result = all(abs(object.vector(:)) > 1.0e-4);
        end
    end
end

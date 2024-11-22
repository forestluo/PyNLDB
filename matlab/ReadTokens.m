% 读取tokens.json文件
json_path = '..\json\';
% 打开文件
[file, message] = fopen(strcat(json_path, 'tokens.json'), 'r');
% 检查结果
if file == -1
    % 显示错误信息
    disp(message);
end

% 字符数组
tokens = [];

% 计数器
count = 0;
% 获得总数
total = 0;
% 百分之一
percent = 0;
one_percent = total / 100.0;

% 循环读取
while ~feof(file)
    % 读取一行
    line = fgetl(file);
    % 循环处理
    while line
        % 剪裁字符串
        line = strip(line);
        % 检查结果
        if length(line) <= 0
            % 读取下一行
            line = fgetl(file);
            continue;
        end

        % 计数器加1
        count = count + 1;
        % 检查计数器
        if count == 1
            % 获得数据总数
            total = str2num(line);
            % 检查结果
            if total <= 0
                % 打印信息
                fprintf('ReadTokens.load : invalid total("%s") !\n' , line);
                break;
            end
            % 更新数组大小
            tokens = zeros(total, 2);
            % 设置百分之一
            one_percent = total / 100.0;
            % 打印数据总数
            fprintf('ReadTokens.load : try to load %d row(s) !\n', total);
        else
            % 解析一行
            item = jsondecode(line);
            % 增加数据
            tokens(count - 1, 1) = item.unicode; % Unicode
            tokens(count - 1, 2) = item.count; % Count
        end

        % 检查结果
        if (count - 1) >= (percent + 1) * one_percent
            % 增加百分之一
            percent = round(percent + 1);
            % 打印进度条         
            fprintf('%d %%\n', percent); %输出进度
        end
        % 检查文件结尾
        if feof(file)
            break;
        end
        % 读取下一行
        line = fgetl(file);
    end
end
% 关闭文件
fclose(file);
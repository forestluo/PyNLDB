% 清理数据
clear

% 维度定义
N = 4;
% 结果记录矩阵
results = [];

% 获得所有字符（不含字符矢量）
words1 = ReadWords("words1.json");
% 转换成词典
tokens = dictionary();
% 循环处理
for i = 1 : size(words1, 1)
    % 检查字符长度
    if strlength(words1(i, 1)) == 1
        % 生成随机矢量
        tokens(words1(i, 1)) = ...
            TokenVector(words1(i, 1), str2double(words1(i, 2)));
    end    
end

% 获得所有双字节词汇（不含字符矢量）
words2 = ReadWords("words2.json");
% 循环处理
for i = 1 : size(words2, 1)
    % 获得词汇
    word = words2(i, 1);
    % 检查长度
    if strlength(word) ~= 2
        fprintf("SolveTokenVectors : long words(%s) !\n", word);
        continue;
    end
    % 获得词频
    f = str2double(words(i, 2));

    % 转换成字节
    word = char(word);
    % 获得两个字符
    c1 = word(1:1); c2 = word(2:2);
    % 查询频次
    f1 = str2double(tokens(c1).count); f2 = str2double(tokens(c2).count);
    % 检查结果
    if f < 0 || f1 <= 0 || f2 <= 0
        fprintf("SolveTokenVectors : invalid words(%s) !\n", word);
        continue;
    end
    % 计算gamma数值
    gamma = 0.5 .* f .* (1 / f1 + 1 / f2);
    % 求解矢量
    VectorSolving(gamma, tokens(c1), tokens(c2), 20)
end

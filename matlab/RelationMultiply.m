% 相关系数乘积
% v1 —— 输入矢量
% v2 —— 输入矢量
% m —— 前后置矩阵维度
function gamma = RelationMultiply(v1, v2, m)
    % 检查参数
    if m < 2
        fprint("RelationMultiply : m(%d)小于2！\n", m);
        return
    end
    l1 = length(v1);
    if l1 <= m
        fpritf("RelationMultiply : v1长度(%d)不大于m(%d)！\n", l1, m);
        return;
    end
    l2 = length(v2);
    if l2 <= m
        fpritf("RelationMultiply : v2长度(%d)不大于m(%d)！\n", l2, m);
        return;
    end
    % 初始化前置矢量
    v3 = v1(1, 1 : m);
    % 初始化后置矢量
    v4 = v2(1, (end - m + 1) : end);
    % 返回结果
    gamma = dot(v3, v4) / (norm(v3) .* norm(v4));
end
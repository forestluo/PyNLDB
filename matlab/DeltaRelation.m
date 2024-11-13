% 求修正误差
% dv1 —— v1的修正误差
% dv2 —— v2的修正误差
% v1 —— 输入矢量
% v2 —— 输入矢量
% m —— 前后置矩阵维度
% delta —— 误差数值
function [dv1, dv2] = DeltaRelation(v1, v2, m, gamma, delta)
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
    % 计算数据
    n1 = norm(v3);
    n2 = norm(v4);
    v10 = v3 / n1;
    v20 = v4 / n2;
    % 计算参数
    L = n2 .* n2 + n1 .* n1;
    C = n1 .* n2 .* delta / (1.0 - gamma);
    Da = n2 .* C / L;
    Db = n1 .* C / L;
    dv1 = [v20 .* Da zeros(1, l1 - m)];
    dv2 = [zeros(1, l2 - m) v10 .* Db];
    %{
    % 计算数据
    n1 = norm(v3);
    n2 = norm(v4);
    v10 = v3 / n1;
    v20 = v4 / n2;
    % 计算参数
    L = n2 .* n2 + n1 .* n1;
    C = n1 .* n2 .* delta / (- gamma);
    Da = n2 .* C / L;
    Db = n1 .* C / L;
    % 求垂直矢量方向
    Av = v3 - (v3 .* v4) .* v20; Av = Av / norm(Av);
    Bv = v4 - (v3 .* v4) .* v10; Bv = Bv / norm(Bv);
    % 求各个分量
    dv1 = [Av .* Da zeros(1, l1 - m)];
    dv2 = [zeros(1, l2 - m) Bv .* Db];
    %}
end
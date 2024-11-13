% 字符关系推算矢量
%向量维数
n = 4;

% 字符'运'
Fa = 937002;
% 字符'运运'
Faa = 343;
% 字符'动'
Fb = 2363927;
% 字符'动动'
Fbb = 1753;
% 字符'运动'
Fab = 175908;
% 字符'动运'
Fba = 1122;

% 相关系数
Gaa = 0.5 * Faa * (1.0 / Fa + 1.0 / Fa);
Gbb = 0.5 * Fbb * (1.0 / Fb + 1.0 / Fb);
Gab = 0.5 * Fab * (1.0 / Fa + 1.0 / Fb);
Gba = 0.5 * Fbb * (1.0 / Fb + 1.0 / Fb);

% 初始化随机向量
Va = rand(1, n);
Vb = rand(1, n);

% 标志位
flag = 0x00;
% 最大次数
MAX_COUNT = 20;
% 循环次数
loop_count = 0;
% 循环处理
while true
    % 清理标志位
    flag = 0x00;
    % 循环次数加一
    loop_count = loop_count + 1;
    % 检查结果
    if loop_count > MAX_COUNT
        % 重置循环计数
        loop_count = 0;
        % 重置初始化矢量
        Va = rand(1, n); Vb = rand(1, n);
    end

    % 保留原值
    Vao = Va; Vbo = Vb;

    % 计数
    count = 0;
    % 循环处理
    while count < MAX_COUNT
        % 计数器加一
        count = count + 1;
        % 求相关系数
        gbb = RelationMultiply2(Vb, Vb, 2);
        % 获得误差
        delta = Gbb - gbb;
        % 检查误差
        if 0 < gbb && abs(delta) < 1.0e-5
            % 设置标记位
            flag = bitor(flag, 0x01);
            % 检查次数
            if count == 1
                % 设置标记位
                flag = bitor(flag, 0x10);
            end
            % 打印信息
            fprintf("Token2Vector2.count(%d) : Δgbb(%f) !\n", count, abs(delta))
            break;
        end
        % 获得误差偏置
        [dv1, dv2] = DeltaRelation2(Vb, Vb, ceil(n / 2), gbb, delta);
        % 设置误差偏置
        Vb = Vb + dv1; Vb = Vb + dv2;
    end
    % 检查标志位
    if bitand(flag, 0x01) == 0
        % 打印信息
        fprintf("Token2Vector2.count(%d) : Δgbb(%f) > 1.0e-5 !\n", count, abs(delta))
    end

    % 计数
    count = 0;
    % 循环处理
    while count < MAX_COUNT
        % 计数器加一
        count = count + 1;
        % 求相关系数
        gaa = RelationMultiply2(Va, Va, ceil(n / 2));
        % 获得误差
        delta = Gaa - gaa;
        % 检查误差
        if 0 < gaa && abs(delta) < 1.0e-5
            % 设置标志位
            flag = bitor(flag, 0x02);
            % 检查次数
            if count == 1
                % 设置标记位
                flag = bitor(flag, 0x20);
            end
            % 打印信息
            fprintf("Token2Vector2.count(%d) : Δgaa(%f) !\n", count, abs(delta))
            break;
        end
        % 获得误差偏置
        [dv1, dv2] = DeltaRelation2(Va, Va, ceil(n / 2), gaa, delta);
        % 设置误差偏置
        Va = Va + dv1; Va = Va + dv2;
    end
    % 检查标志位
    if bitand(flag, 0x02) == 0
        % 打印信息
        fprintf("Token2Vector2.count(%d) : Δgaa(%f) > 1.0e-5 !\n", count, abs(delta))
    end
    
    % 计数
    count = 0;
    % 循环处理
    while count < MAX_COUNT
        % 计数器加一
        count = count + 1;
        % 求相关系数
        gab = RelationMultiply2(Va, Vb, ceil(n / 2));
        % 获得误差
        delta = Gab - gab;
        % 检查误差
        if 0 < gab && abs(delta) < 1.0e-5
            % 设置标志位
            flag = bitor(flag, 0x04);
            % 检查次数
            if count == 1
                % 设置标记位
                flag = bitor(flag, 0x40);
            end
            % 打印信息
            fprintf("Token2Vector2.count(%d) : Δgab(%f) !\n", count, abs(delta))
            break;
        end
        % 获得误差偏置
        [dv1, dv2] = DeltaRelation2(Va, Vb, ceil(n / 2), gab, delta);
        % 设置误差偏置
        Va = Va + dv1; Vb = Vb + dv2;
    end
    % 检查标志位
    if bitand(flag, 0x04) == 0
        % 打印信息
        fprintf("Token2Vector2.count(%d) : Δgab(%f) > 1.0e-5 !\n", count, abs(delta))
    end

    % 计数
    count = 0;
    % 循环处理
    while count < MAX_COUNT
        % 计数器加一
        count = count + 1;
        % 求相关系数
        gba = RelationMultiply2(Vb, Va, ceil(n / 2));
        % 获得误差
        delta = Gba - gba;
        % 检查误差
        if 0 < gba && abs(delta) < 1.0e-5
            % 设置标志位
            flag = bitor(flag, 0x08);
            % 检查次数
            if count == 1
                % 设置标记位
                flag = bitor(flag, 0x80);
            end
            % 打印信息
            fprintf("Token2Vector2.count(%d) : Δgba(%f) !\n", count, abs(delta))
            break;
        end
        % 获得误差偏置
        [dv1, dv2] = DeltaRelation2(Vb, Va, ceil(n / 2), gba, delta);
        % 设置误差偏置
        Vb = Vb + dv1; Va = Va + dv2;
    end
    % 检查标志位
    if bitand(flag, 0x08) == 0
        % 打印信息
        fprintf("Token2Vector2.count(%d) : Δgba(%f) > 1.0e-5 !\n", count, abs(delta))
    end

    % 检查距离
    if bitand(flag, 0x0F) ~= 0x0F
        % 设置循环次数，要求重置
        flag = 0x00; loop_count = MAX_COUNT;
    % 全部一次性达到要求
    elseif bitand(flag, 0xF0) == 0xF0
        % 检查距离变化
        if pdist2(Vao, Va) < 1.0e-5 && pdist2(Vbo, Vb) < 1.0e-5
            % 打印信息
            fprintf("Token2Vector2 : dist(Vao, Va) = %f !\n", pdist2(Vao, Va))
            fprintf("Token2Vector2 : dist(Vbo, Vb) = %f !\n", pdist2(Vbo, Vb))
            % 检查距离，并且每个元素不能过小
            if pdist2(Va, Vb) > 1.0e3 || ...
                not (all(abs(Va(:)) > 1.0e-4) && all(abs(Vb(:)) > 1.0e-4))
                % 设置循环次数，要求重置
                flag = 0x00; loop_count = MAX_COUNT;
            else
                % 打印信息
                fprintf("Token2Vector2 : show results !\n")
                fprintf("\tVa = \b"); disp(Va);
                fprintf("\tVb = \b"); disp(Vb);
                fprintf("\tΔ(ab) = %f !\n", pdist2(Va, Vb));
                fprintf("\tΓ(aa) = %f (Gaa = %f)\n", RelationMultiply2(Va, Va, ceil(n / 2)), Gaa);
                fprintf("\tΓ(bb) = %f (Gbb = %f)\n", RelationMultiply2(Vb, Vb, ceil(n / 2)), Gbb);
                fprintf("\tΓ(ab) = %f (Gab = %f)\n", RelationMultiply2(Va, Vb, ceil(n / 2)), Gab);
                fprintf("\tΓ(ba) = %f (Gba = %f)\n", RelationMultiply2(Vb, Va, ceil(n / 2)), Gba);
                break;
            end
        end
    end
end

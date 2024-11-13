function [gamma, delta] = VectorSolving(Gamma, Tv1, Tv2, MAX_COUNT)
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
            Tv1.Reset(); Tv2.Reset();
        end
        
        % 保留原值
        Tv1.Backup(); Tv2.Bakcup();

        % 计数
        count = 0;
        % 循环处理
        while count < MAX_COUNT
            % 计数器加一
            count = count + 1;
            % 求相关系数
            gamma = RelationMultiply2(Tv1.vector, Tv2.vector, ceil(TokenVector.N / 2));
            % 获得误差
            delta = Gamma - gamma;
            % 检查误差
            if 0 < gamma && abs(delta) < 1.0e-5
                % 设置标记位
                flag = bitor(flag, 0x01);
                % 检查次数
                if count == 1
                    % 设置标记位
                    flag = bitor(flag, 0x10);
                end
                % 打印信息
                fprintf("VectorSolving.count(%d) : Δgamma(%f) !\n", count, abs(delta))
                break;
            end
            % 获得误差偏置
            [dv1, dv2] = DeltaRelation2(Tv1.vector, Tv2.vector, ceil(TokenVector.N / 2), gamma, delta);
            % 设置误差偏置
            Tv1.vector = Tv1.vector + dv1; Tv2.vector = Tv2.vector + dv2;
        end
        % 检查标志位
        if bitand(flag, 0x01) == 0
            % 打印信息
            fprintf("VectorSolving.count(%d) : Δgamma(%f) > 1.0e-5 !\n", count, abs(delta))
        end

        % 检查距离
        if bitand(flag, 0x01) ~= 0x01
            % 设置循环次数，要求重置
            loop_count = MAX_COUNT;
        % 全部一次性达到要求
        elseif bitand(flag, 0x10) == 0x10
            % 检查距离变化
            if Tv1.Error() < 1.0e-5 && Tv2.Error() < 1.0e-5
                % 检查距离，并且每个元素不能过小
                if pdist2(Tv1.vector, Tv2.vector) > 1.0e3 || ...
                    not (Tv1.NoSmallValue() && Tv2.NoSmallValue())
                    % 设置循环次数，要求重置
                    loop_count = MAX_COUNT;
                else
                    % 打印信息
                    fprintf("VectorSolving : show results !\n")
                    fprintf("\tV1 ="); disp(Tv1.vector);
                    fprintf("\tV2 ="); disp(Tv2.vector);
                    fprintf("\tΔ(12) = %f !\n", delta);
                    fprintf("\tΓ(12) = %f (G12 = %f)\n", gamma, Gamma);
                    % 打印信息
                    fprintf("VectorSolving : error(V10, V1) = %f !\n", Tv1.Error())
                    fprintf("VectorSolving : error(V20, V2) = %f !\n", Tv2.Error())
                    break;
                end
            end
        end
    end
end
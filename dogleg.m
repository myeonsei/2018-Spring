x1 = -20; x2 = 15; a = 10^-4; d = .4; tol = 10^-8; dist = 1; cnt = 0;
fprintf('STEP       x1         x2         fx         d\n')
fprintf('START      %.8f %.8f %.8f %.8f\n',x1,x2,f(x1,x2),d)
while dist > tol
    [s d newton] = s_dogleg(x1, x2, d);
    f_o = f(x1, x2); df_o = df(x1, x2); f_n = f(x1+s(1), x2+s(2));
    cnt = cnt + 1;
    pause(1);
    fprintf('[%.2d, A]    %.8f %.8f %.8f %.8f\n',cnt,x1+s(1),x2+s(2),f_n,d)
    while f_n > f_o + a * df_o' * s
       l = - 0.5 * df_o' * s / (f_n - f_o - df_o' * s);
       
       if l < 0.1
           l = 0.1;
       elseif l > 0.5
           l = 0.5;
       end
       
       d = l * d;
       [s d newton] = s_dogleg(x1, x2, d);
       f_n = f(x1+s(1), x2+s(2));
       cnt = cnt + 1;
       pause(1);
       fprintf('[%.2d, B]    %.8f %.8f %.8f %.8f\n', cnt, x1+s(1),x2+s(2),f_n,d)
       %disp(['STUCK1'])
    end
    
    if newton == 0
        real_df = f_n - f_o;
        pred_df = mc(x1, x2, s) - f_o;
        if abs(pred_df - real_df) <= 0.1 * abs(real_df) || real_df <= df_o' * s
            fl = 1;
            while fl == 1
                d = 2 * d;
                [s_n d newton] = s_dogleg(x1, x2, d);
                f_n = f(x1+s_n(1), x2+s_n(2));
                if f_n <= f_o + a * df_o' * s_n
                    s = s_n;
                    if newton == 1
                        fl = 0;
                    end
                    cnt = cnt + 1;
                    pause(1);
                    fprintf('[%.2d, C]    %.8f %.8f %.8f %.8f\n',cnt,x1+s(1),x2+s(2),f_n,d)
                else
                    fl = 0;
                    d = d / 2;
                end
                
            end
        end
    end
    
    real_df = f(x1+s(1), x2+s(2)) - f_o;
    pred_df = mc(x1, x2, s) - f_o; 
    
    if real_df <= 0.75 * pred_df
        d = 2 * d;
        cnt = cnt + 1;
        pause(1);
        fprintf('[%.2d, D]    %.8f %.8f %.8f %.8f\n',cnt,x1+s(1),x2+s(2),f_n,d)
    elseif real_df > 0.1 * pred_df
        d = 0.5 * d;
        cnt = cnt + 1;
        pause(1);
        fprintf('[%.2d, D]    %.8f %.8f %.8f %.8f\n',cnt,x1+s(1),x2+s(2),f_n,d)
    end
    
    dist = norm(s, 2);
    x1 = x1 + s(1); x2 = x2 + s(2);
    
    %disp(['ONE LOOP DONE'])
end

function fx = f(x1, x2) % return f(x)
    fx = (x1-1)^4 + (x1-1)^2 + (x2-5)^2;
end

function dfx = df(x1, x2) % return gradient of f
    dfx = [4*((x1-1)^3)+2*(x1-1), 2*(x2-5)]';
end

function ddfx = ddf(x1, x2) % return hessian of f
    ddfx = [12*((x1-1)^2)+2, 0; 0, 2];
end

function h = hessian(x1, x2) % return adjusted hessian of f
    h = ddf(x1, x2);
    evs = eig(h);
    if min(evs) == 0
       h = h + 10^-4 * eye(2);
    elseif min(evs) < 0
       h = h + abs(min(evs)) * 1.1 * eye(2);
    end
end

function m = mc(x1, x2, s)
    m = f(x1, x2) + df(x1, x2)' * s + 0.5 * s' * hessian(x1, x2) * s;
end

function s = scp(x1, x2) % return cautchy step
    dfx = df(x1, x2);
    hexx = hessian(x1, x2);
    s = -((dfx' * dfx) / (dfx' * hexx * dfx)) * dfx;
end

function s = sn(x1, x2) % return newton step
    dfx = df(x1, x2);
    hex = hessian(x1, x2);
    s = -inv(hex) * dfx;
end

function [s d_new newton] = s_dogleg(x1, x2, d) % find dogleg step when d imposed
    snew = sn(x1, x2);
    scau = scp(x1, x2);
    if norm(snew, 2) <= d
        s = snew;
        d_new = norm(snew, 2);
        newton = 1;
    elseif norm(scau, 2) >= d
        s = d / norm(scau, 2) * scau;
        d_new = d;
        newton = 0;
    else
        ds = snew - scau;
        l = (-scau' * ds + sqrt((scau' * ds) ^ 2 - (scau' * scau - d^2) * ds' * ds)) / (ds' * ds);
        s = scau + l * ds;
        d_new = d;
        newton = 0;
    end
end

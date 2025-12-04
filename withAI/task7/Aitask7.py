import torch
import torch.nn as nn

class AttnBlock(nn.Module):
    """
    单头自注意力机制模块（Single-Head Self-Attention）
    核心功能：捕捉序列中每个位置与所有位置（包括自身）的依赖关系，
              通过加权求和聚合相关信息（自注意力=Q/K/V均来自同一输入）
    数学基础：基于"查询-键-值"（Query-Key-Value）注意力框架
    """
    def __init__(self, d_model, d_k=64):
        """
        初始化单头注意力模块（参数映射+可学习参数定义）
        参数说明：
            d_model (int): 输入特征维度（如Transformer标准512），即每个序列位置的特征向量维度
            d_k (int): Q/K/V的特征维度（默认64），是注意力计算的核心维度
        数学逻辑：输入X ∈ [batch_size, seq_len, d_model]，需通过线性变换映射到Q/K/V空间
        """
        # 必须调用父类nn.Module的构造函数，让PyTorch管理模块参数（权重、偏置）、训练模式等
        super(AttnBlock, self).__init__()
        
        # 1. 生成查询Q的线性层：W_q ∈ [d_model, d_k]，偏置b_q ∈ [d_k]
        # 数学表达式：Q = X · W_q + b_q （矩阵乘法+广播加法）
        # 作用：将d_model维输入特征，投影到d_k维，学习"查询"相关的特征映射
        self.fc_q = nn.Linear(d_model, d_k)
        
        # 2. 生成键K的线性层：W_k ∈ [d_model, d_k]，偏置b_k ∈ [d_k]
        # 数学表达式：K = X · W_k + b_k
        # 作用：将d_model维输入特征，投影到d_k维，学习"键"相关的特征映射
        self.fc_k = nn.Linear(d_model, d_k)
        
        # 3. 生成值V的线性层：W_v ∈ [d_model, d_k]，偏置b_v ∈ [d_k]
        # 数学表达式：V = X · W_v + b_v
        # 作用：将d_model维输入特征，投影到d_k维，学习"值"相关的特征映射
        self.fc_v = nn.Linear(d_model, d_k)
        
        # 保存d_k：为后续注意力分数缩放提供参数（核心数学操作的依赖）
        self.d_k = d_k

    def forward(self, x):
        """
        前向传播：完整计算注意力加权输出（核心流程+数学运算）
        参数：
            x (torch.Tensor): 输入张量，形状[batch_size, seq_len, d_model]
                batch_size：批量大小（一次处理的样本数）
                seq_len：序列长度（每个样本的token个数）
                d_model：每个token的特征维度
        返回：
            output (torch.Tensor): 注意力加权输出，形状[batch_size, seq_len, d_k]
                每个token的特征更新为"自身与所有token的相关信息聚合结果"
            weights (torch.Tensor): 注意力权重矩阵，形状[batch_size, seq_len, seq_len]
                weights[i,j,k]：第i个样本中，第j个位置对第k个位置的依赖权重
        """
        # -------------------------- 步骤1：线性变换生成Q、K、V --------------------------
        # 输入x：[batch_size, seq_len, d_model]
        # 线性变换后，Q/K/V均映射为d_k维，形状统一为[batch_size, seq_len, d_k]
        # 数学意义：将原始特征投影到"查询-键-值"三个独立空间，适配注意力计算
        Q = self.fc_q(x)  # Q: 查询矩阵 → 每个位置"要找什么信息"
        K = self.fc_k(x)  # K: 键矩阵 → 每个位置"提供什么信息"
        V = self.fc_v(x)  # V: 值矩阵 → 每个位置"实际的信息内容"

        # -------------------------- 步骤2：计算注意力分数（QK^T）并缩放 --------------------------
        # 2.1 转置K矩阵：K原本是[batch_size, seq_len, d_k]，转置最后两维后为[batch_size, d_k, seq_len]
        # 转置原因：矩阵乘法要求"前矩阵列数=后矩阵行数"，Q的列数是d_k，需K的行数为d_k才能点积
        K_t = K.transpose(-2, -1)  # -2表示倒数第二维，-1表示倒数第一维
        
        # 2.2 点积计算相似度：Q @ K_t（等价于torch.matmul(Q, K_t)）
        # 维度变化：[B, L, d_k] × [B, d_k, L] → [B, L, L]（B=batch_size，L=seq_len）
        # 数学意义：attn_scores[i,j,k] = Q[i,j,:] · K[i,k,:]（第i个样本，j位置查询与k位置键的内积）
        # 内积性质：值越大，说明Q[j]和K[k]的语义相似度越高，依赖关系越强
        attn_scores = Q @ K_t
        
        # 2.3 缩放操作：除以√d_k（核心数学优化，避免梯度消失）
        # 数学推导：
        # 假设Q和K的元素均服从均值=0、方差=1的正态分布，则Q[i,j,:]·K[i,k,:]的方差为d_k：
        # Var(Q·K^T) = Var(Σ_{t=1 to d_k} Q_t K_t) = Σ_{t=1 to d_k} Var(Q_t K_t) = d_k×1 = d_k（Q和K独立）
        # 若d_k较大（如64），QK^T的元素值会集中在±√d_k（如±8），代入softmax后会"两极分化"（概率接近0或1）
        # 导致softmax梯度趋近于0（梯度消失），模型无法训练
        # 缩放后：Var(attn_scores/√d_k) = d_k / d_k = 1，元素值落在±1附近，softmax梯度正常
        scaled_scores = attn_scores / torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))

        # -------------------------- 步骤3：softmax生成注意力权重 --------------------------
        # 对scaled_scores的最后一维（seq_len维度）做softmax：每行归一化
        # 维度变化：[B, L, L] → [B, L, L]（每行元素和为1，且均非负）
        # 数学公式：weights[i,j,k] = exp(scaled_scores[i,j,k]) / Σ_{t=1 to L} exp(scaled_scores[i,j,t])
        # 物理意义：将相似度分数转换为"注意力分配概率"，weights[i,j,k]表示第j个位置对第k个位置的关注程度
        weights = torch.softmax(scaled_scores, dim=-1)

        # -------------------------- 验证环节：确保计算逻辑正确 --------------------------
        self._validate(scaled_scores, weights)

        # -------------------------- 步骤4：权重加权求和V，得到最终输出 --------------------------
        # 矩阵乘法：weights × V
        # 维度变化：[B, L, L] × [B, L, d_k] → [B, L, d_k]
        # 数学意义：output[i,j,:] = Σ_{k=1 to L} weights[i,j,k] × V[i,k,:]
        # 物理意义：第j个位置的输出 = 所有位置的V特征，按注意力权重加权平均（关注程度越高，权重越大）
        output = weights @ V
        
        # 返回更新后的特征和注意力权重（权重可用于可视化依赖关系）
        return output, weights

    def _validate(self, scaled_scores, weights):
        """
        验证注意力计算的正确性（从数学性质和维度合法性角度校验）
        避免因维度错误、数值异常导致模型训练失败
        """
        # 验证1：缩放后分数的形状必须是方阵（自注意力的核心性质）
        # 原因：Q和K均来自同一输入x，序列长度相同（L_q = L_k = seq_len），故QK^T形状为[B, L, L]
        batch_size, seq_len_q, seq_len_k = scaled_scores.shape
        assert seq_len_q == seq_len_k, f"自注意力中Q和K序列长度必须一致！当前Q长度={seq_len_q}，K长度={seq_len_k}"
        print("✅ 验证1：QK^T / sqrt(d_k) 计算正确（形状为方阵[batch_size, seq_len, seq_len]）")

        # 验证2：注意力权重必须是合法的概率分布（softmax的核心性质）
        # 条件1：所有权重非负（softmax输出天然满足，但需防止数值溢出导致的异常）
        assert torch.all(weights >= -1e-6), "注意力权重必须非负！出现负权重可能是数值溢出"
        # 条件2：每行权重和接近1（允许1e-6的误差，因浮点计算精度问题）
        row_sums = torch.sum(weights, dim=-1)  # 对最后一维求和，得到[B, L]的行和向量
        # torch.isclose：判断两个张量是否在允许误差内相等（atol=1e-6：绝对误差容忍度）
        assert torch.all(torch.isclose(row_sums, torch.ones_like(row_sums), atol=1e-6)), \
            f"注意力权重每行和应接近1！当前行和范围：[{row_sums.min():.6f}, {row_sums.max():.6f}]"
        print("✅ 验证2：softmax权重为合法概率分布（非负且每行和≈1）")

# 测试代码：实际运行模块，观察输入输出形状和数值，验证逻辑正确性
if __name__ == "__main__":
    # 1. 固定随机种子：让每次运行的随机数相同，结果可复现（方便调试）
    torch.manual_seed(42)
    
    # 2. 定义测试参数（模拟真实场景的输入维度）
    batch_size = 2  # 一次处理2个样本
    seq_len = 5     # 每个样本有5个token（如5个单词）
    d_model = 512   # 每个token的特征维度（Transformer标准配置）
    
    # 3. 生成模拟输入：随机张量（符合正态分布N(0,1)），形状[2,5,512]
    # 实际场景中，x是嵌入层（Embedding）+ 位置编码（Positional Encoding）的输出
    x = torch.randn(batch_size, seq_len, d_model)
    
    # 4. 初始化注意力模块：输入维度d_model=512，Q/K/V维度d_k=64
    attn_block = AttnBlock(d_model=d_model, d_k=64)
    
    # 5. 前向传播：得到输出和注意力权重
    output, weights = attn_block(x)

    # 6. 打印核心信息：验证维度是否符合预期
    print("\n" + "="*50)
    print("核心维度验证（预期vs实际）：")
    print(f"输入形状：{x.shape} → 预期[batch_size, seq_len, d_model] = [{batch_size}, {seq_len}, {d_model}]")
    # 修复：Q是forward里的局部变量，全局无法访问，改为文字说明预期形状（实际运行中Q/K/V形状已在forward内保证正确）
    print(f"Q/K/V形状：预期[batch_size, seq_len, d_k] = [{batch_size}, {seq_len}, 64]（forward内线性变换后自动满足）")
    print(f"注意力权重形状：{weights.shape} → 预期[batch_size, seq_len, seq_len] = [{batch_size}, {seq_len}, {seq_len}]")
    print(f"输出形状：{output.shape} → 预期[batch_size, seq_len, d_k] = [{batch_size}, {seq_len}, 64]")
    
    # 7. 打印具体数值：直观观察权重和输出的特点
    print("\n" + "="*50)
    print("第一个样本的注意力权重矩阵（前3行3列，保留3位小数）：")
    # detach()：脱离计算图（无需计算梯度），numpy()：转换为numpy数组（方便打印）
    print(weights[0, :3, :3].detach().numpy().round(3))
    # 权重解读：比如weights[0,0,1]=0.23 → 第一个样本的第0个token对第1个token的关注程度为23%
    
    print("\n" + "="*50)
    print("第一个样本的输出（前2个位置，前3个特征，保留3位小数）：")
    print(output[0, :2, :3].detach().numpy().round(3))
    # 输出解读：每个位置的特征是所有位置V的加权平均，体现了全局依赖信息
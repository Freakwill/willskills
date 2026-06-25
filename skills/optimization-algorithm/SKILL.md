---
name: optimization-algorithm
description: Design and improve optimization algorithms for operations research (linear programming, integer programming, nonlinear programming, convex optimization) and machine learning (SGD, Adam, BP, EM, Monte Carlo methods, MCMC). Improve classic algorithms with modern techniques, implement novel methods from recent arXiv papers, and solve constrained/unconstrained optimization problems with rigorous benchmarking. Use this skill whenever the user asks about optimization algorithms, solver design, convergence analysis, algorithm improvement, or implementing optimization methods from research papers — even if they don't explicitly name the technique.
version: 0.1
---

# Optimization Algorithm Design Skill

A comprehensive skill for designing, analyzing, implementing, and benchmarking optimization algorithms across both traditional operations research and modern machine learning domains. Targeted at researchers and practitioners who need rigorous, reproducible algorithm development.

---

## Problem Taxonomy

### 1. Continuous Optimization
| Class | Canonical Form | Key Properties |
|---|---|---|
| **Linear Programming (LP)** | min cᵀx s.t. Ax ≤ b, x ≥ 0 | Linear objective, linear constraints, convex, polyhedral feasible set |
| **Quadratic Programming (QP)** | min ½xᵀQx + cᵀx s.t. Ax ≤ b | Quadratic objective (Q ≽ 0 convex, Q indefinite hard) |
| **Convex Optimization** | min f₀(x) s.t. fᵢ(x) ≤ 0, Ax = b | All fᵢ convex → global optimum guaranteed |
| **Nonlinear Programming (NLP)** | min f(x) s.t. h(x) = 0, g(x) ≤ 0 | Non-convex possible, multiple local optima |
| **Semidefinite Programming (SDP)** | min C∙X s.t. Aᵢ∙X = bᵢ, X ≽ 0 | Linear over PSD cone, SDP duality |

### 2. Discrete / Combinatorial Optimization
| Class | Description | Typical Solution Approach |
|---|---|---|
| **Integer Programming (IP/MIP)** | Variables constrained to ℤ⁺ | Branch-and-Bound, Cutting Planes, Branch-and-Cut |
| **Combinatorial Optimization** | TSP, VRP, graph problems | Exact: Branch-and-Bound; Heuristic: LKH, Guided Local Search |
| **Stochastic Programming** | Optimization under uncertainty | Scenario-based, Sample Average Approximation, Robust Optimization |

### 3. Stochastic / Derivative-Free Optimization
| Class | Description | Typical Methods |
|---|---|---|
| **Monte Carlo Methods** | Random sampling for estimation/optimization | MC integration, Importance Sampling, Sequential MC |
| **MCMC** | Sampling from complex distributions | Metropolis-Hastings, HMC, NUTS, Gibbs Sampling |
| **Evolutionary Algorithms** | Population-based black-box optimization | GA, ES, CMA-ES, Differential Evolution |
| **Simulation Optimization** | Objective = stochastic simulation | RSM, Optimal Computing Budget Allocation |


## Algorithm Families & State of the Art

### First-Order Methods (ML focus)
| Algorithm | Convergence (Convex) | Key Variant / Improvement | Reference |
|---|---|---|---|
| **SGD** | O(1/√T) | SGD with momentum, Polyak | Robbins & Monro (1951) |
| **SGD with Momentum** | O(1/T) for strong convex | Nesterov accelerated gradient | Polyak (1964), Nesterov (1983) |
| **AdaGrad** | O(1/√T) | Adaptive per-parameter LR | Duchi et al. (2011) |
| **RMSProp** | — | Moving average of squared gradients | Hinton (2012, lecture) |
| **Adam** | O(1/√T) | AMSGrad, AdamW, AdaBelief | Kingma & Ba (2015) |
| **AdamW** | — | Decoupled weight decay | Loshchilov & Hutter (2019) |
| **LAMB** | — | Layer-wise adaptive LR for large batch | You et al. (2020) |
| **Shampoo** | — | Preconditioner via Kronecker-factored stats | Gupta et al. (2018) |
| **Sophia** | — | Second-order clipping for LLM pre-training | Liu et al. (2024) |

### Second-Order Methods
| Algorithm | Cost/iter | Key Property | Best For |
|---|---|---|---|
| **Newton's method** | O(n³) | Quadratic convergence near optimum | Small n, smooth f |
| **BFGS / L-BFGS** | O(n²) / O(n) | Approximate Newton, quasi-Newton | Medium-scale deterministic |
| **Trust Region (TR)** | O(n³) per subproblem | Global convergence guarantees | Ill-conditioned problems |
| **Gauss-Newton** | O(n³) | Exploits least-squares structure | Nonlinear least squares |
| **Natural Gradient** | O(n²) | Fisher information metric | Variational inference, RL |
| **K-FAC** | O(n³) blocks | Kronecker-factored approximate curvature | Deep learning (blocks) |

### Integer / Combinatorial Methods
| Method | Type | State-of-the-Art |
|---|---|---|
| **Branch-and-Bound** | Exact | SCIP, Gurobi, CPLEX (with presolve, cutting planes, heuristics) |
| **Branch-and-Cut** | Exact | Combines B&B with cutting plane generation |
| **Branch-and-Price** | Exact | Column generation + B&B (decomposition) |
| **Lazy Constraints** | Exact | Callback-added constraints as needed |
| **Local Search** | Heuristic | Guided Local Search, Tabu Search |
| **Large Neighborhood Search** | Heuristic | Destroy-and-repair operators |
| **LKH (Lin-Kernighan)** | Heuristic | State-of-the-art for TSP |
| **Hybrid GA** | Metaheuristic | GA + Local Search (memetic algorithms) |

### Monte Carlo & Sampling Methods
| Method | Description | Advanced Variant |
|---|---|---|
| **Metropolis-Hastings** | Accept/reject with proposal distribution | Adaptive MCMC, DRAM |
| **Hamiltonian Monte Carlo (HMC)** | Uses gradient information for efficient exploration | NUTS (No-U-Turn Sampler) |
| **Gibbs Sampling** | Conditional sampling for graphical models | Collapsed Gibbs, Block Gibbs |
| **Sequential Monte Carlo (SMC)** | Particle filtering for state-space models | Adaptive SMC, Resample-Move |
| **Variance Reduction** | Control variates, antithetic variables, Rao-Blackwellization | Delayed Acceptance |

---

## Workflow: Algorithm Design & Implementation

### Phase 1: Problem Analysis
```
1. Identify: variables, objective f(x), constraints g(x) ≤ 0, h(x) = 0
2. Classify:
   - Is f linear, quadratic, convex, smooth, stochastic?
   - Are constraints present? Linear/nonlinear?
   - Variable domain: ℝⁿ, ℤⁿ, mixed, manifold?
   - Problem scale: n ≈ ? m ≈ ?
3. Determine hardness:
   - Convex → global optimum tractable
   - Non-convex → stationarity, structure exploitation
   - NP-hard → heuristics, approximation guarantees
4. Choose success metric: optimality gap, runtime, memory, sample efficiency
```

### Phase 2: Algorithm Selection / Design
```
For each problem class:
  Convex + smooth + small → Newton / BFGS / L-BFGS
  Convex + smooth + large → SGD / Adam / L-BFGS
  Convex + non-smooth → Subgradient / Proximal / ADMM
  Non-convex + smooth → AdamW / SGD + momentum / Sophia
  LP / QP → Simplex / Interior Point (via scipy, Gurobi, CPLEX)
  MILP → Branch-and-Cut (via SCIP, Gurobi, pulp)
  SDP → SDPT3 / MOSEK / CVXPY
  Black-box → CMA-ES / Bayesian Optimization / Evolutionary
  Sampling → HMC / NUTS / PyMC

To design a new variant:
  1. Identify failure mode of existing algorithm
  2. Propose modification (e.g., new adaptive step size, different preconditioner)
  3. Prove/argue for convergence (or at least bounded divergence)
  4. Implement and benchmark
```

### Phase 3: Implementation (Python)
Use the templates below. For each implementation, include:
- **Reproducibility**: fix random seed, save hyperparameters, log all intermediate states
- **Numerical stability**: gradient clipping, nan/inf checks, log-sum-exp trick
- **Performance**: vectorize with NumPy/PyTorch, profile with cProfile

### Phase 4: Verification & Benchmarking
- **Convergence**: log objective f(xₖ) vs iteration; compare to known optimum
- **Statistical testing**: for stochastic algorithms, report mean ± std over ≥5 runs with different seeds
- **Scalability**: wall-clock time vs problem dimension n
- **Comparison**: against standard baselines (SciPy, PyTorch optimizers, Gurobi)


## Python Templates (Researcher-Grade)

### 1. Linear Programming — Simplex vs Interior Point
```python
import numpy as np
from scipy.optimize import linprog, minimize
import time, matplotlib.pyplot as plt

def benchmark_lp_solvers():
    """Compare HiGHS simplex vs interior-point on random LPs."""
    np.random.seed(42)
    results = {}
    for n in [10, 50, 100, 500]:
        c = np.random.randn(n)
        m = n // 2
        A = np.random.randn(m, n)
        b = np.random.randn(m) + 10  # ensure feasibility
        for method in ['highs', 'highs-ipm', 'highs-ds']:
            start = time.perf_counter()
            res = linprog(c, A_ub=A, b_ub=b, method=method, options={'maxiter': 10000})
            elapsed = time.perf_counter() - start
            results[(n, method)] = {'status': res.status, 'fun': res.fun, 'time': elapsed}
    return results
```

### 2. Convex Optimization — Custom Proximal Gradient Method
```python
import numpy as np

def proximal_gradient(f, grad_f, prox_g, x0, L, max_iter=1000, tol=1e-8):
    """
    min f(x) + g(x) where f is smooth, g is prox-capable.
    f: smooth function
    grad_f: gradient of f
    prox_g: proximal operator of g
    L: Lipschitz constant of grad_f (or backtrack)
    """
    x = x0.copy()
    history = [x.copy()]
    for k in range(max_iter):
        x_new = prox_g(x - (1.0 / L) * grad_f(x), 1.0 / L)
        history.append(x_new.copy())
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    return x, np.array(history)
```
For FISTA (fast ISTA), add momentum extrapolation:
```python
def fista(f, grad_f, prox_g, x0, L, max_iter=1000):
    x = x0.copy()
    y = x0.copy()
    t = 1.0
    history = []
    for k in range(max_iter):
        x_old = x.copy()
        x = prox_g(y - (1.0 / L) * grad_f(y), 1.0 / L)
        t_new = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
        y = x + ((t - 1.0) / t_new) * (x - x_old)
        t = t_new
        history.append(f(x))
    return x, history
```

### 3. Stochastic Optimizer — Custom Adam Variant
```python
import torch

class CustomAdam(torch.optim.Optimizer):
    """
    Adam with adaptive beta scheduling and gradient clipping.
    Reference: Kingma & Ba (2015), improved clipping from Pre-LN.
    """
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8,
                 weight_decay=0.0, clip_norm=1.0):
        defaults = dict(lr=lr, betas=betas, eps=eps,
                       weight_decay=weight_decay, clip_norm=clip_norm)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            beta1, beta2 = group['betas']
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                if group['clip_norm'] > 0:
                    torch.nn.utils.clip_grad_norm_(p, group['clip_norm'])
                state = self.state[p]
                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p)
                    state['exp_avg_sq'] = torch.zeros_like(p)
                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                state['step'] += 1
                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']
                if group['weight_decay'] > 0:
                    grad = grad.add(p, alpha=group['weight_decay'])
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
                denom = (exp_avg_sq.sqrt() / np.sqrt(bias_correction2)).add_(group['eps'])
                step_size = group['lr'] / bias_correction1
                p.addcdiv_(exp_avg, denom, value=-step_size)
        return loss
```

### 4. EM Algorithm — Mixture of Gaussians (Custom)
```python
import numpy as np
from scipy.stats import multivariate_normal

def em_gmm(X, K, max_iter=100, tol=1e-6):
    """
    EM for Gaussian Mixture Model.
    E-step: compute responsibilities
    M-step: update means, covariances, mixing coefficients
    """
    n, d = X.shape
    # Initialize via k-means++
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=K, random_state=42).fit(X)
    means = kmeans.cluster_centers_
    covs = np.array([np.cov(X[labels == k].T) + 1e-6 * np.eye(d)
                     for k in range(K)])
    pis = np.ones(K) / K
    log_likelihoods = []
    for iteration in range(max_iter):
        # E-step
        resp = np.zeros((n, K))
        for k in range(K):
            try:
                resp[:, k] = pis[k] * multivariate_normal.pdf(X, means[k], covs[k])
            except np.linalg.LinAlgError:
                resp[:, k] = 0.0
        resp /= resp.sum(axis=1, keepdims=True)
        # M-step
        Nk = resp.sum(axis=0)
        pis = Nk / n
        means = (resp.T @ X) / Nk[:, None]
        for k in range(K):
            diff = X - means[k]
            covs[k] = (resp[:, k:k+1] * diff).T @ diff / Nk[k]
            covs[k] += 1e-6 * np.eye(d)
        # Log-likelihood
        ll = np.sum(np.log(np.sum(resp, axis=1)))
        log_likelihoods.append(ll)
        if iteration > 0 and abs(ll - log_likelihoods[-2]) < tol:
            break
    return means, covs, pis, log_likelihoods
```

### 5. MCMC — Hamiltonian Monte Carlo
```python
import numpy as np

def hmc_sample(U, grad_U, eps=0.05, L=10, q0=0.0, n_samples=1000):
    """
    Hamiltonian Monte Carlo sampling.
    U: potential energy = -log p(q) (up to constant)
    grad_U: gradient of U
    eps: step size (leapfrog)
    L: number of leapfrog steps per trajectory
    """
    q = np.array(q0, dtype=float)
    samples = [q.copy()]
    accept_count = 0
    for _ in range(n_samples):
        p = np.random.normal(size=q.shape)  # momentum: p ~ N(0, I)
        q_current, p_current = q.copy(), p.copy()
        H_start = U(q_current) + 0.5 * np.sum(p_current**2)
        # Leapfrog
        p_current -= 0.5 * eps * grad_U(q_current)
        for _ in range(L - 1):
            q_current += eps * p_current
            p_current -= eps * grad_U(q_current)
        q_current += eps * p_current
        p_current -= 0.5 * eps * grad_U(q_current)
        H_end = U(q_current) + 0.5 * np.sum(p_current**2)
        # Metropolis accept/reject
        if np.random.random() < np.exp(H_start - H_end):
            q = q_current
            accept_count += 1
        samples.append(q.copy())
    accept_rate = accept_count / n_samples
    return np.array(samples), accept_rate
```


## ArXiv Paper Integration

### Search & Summarize
```python
import requests, xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 10, categories: list = None):
    """
    Search arXiv for recent optimization papers.
    Categories: cs.OC, math.OC, stat.ML, cs.LG, math.NA
    """
    cat_filter = '(' + '+OR+'.join(f'cat:{c}' for c in (categories or ['cs.OC','math.OC','stat.ML'])) + ')'
    search_query = f'all:{query}+AND+{cat_filter}'
    url = f'http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    resp = requests.get(url, timeout=15)
    root = ET.fromstring(resp.text)
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('a:entry', ns):
        papers.append({
            'id': entry.find('a:id', ns).text.strip(),
            'title': entry.find('a:title', ns).text.strip().replace('\n', ' '),
            'authors': [a.find('a:name', ns).text for a in entry.findall('a:author', ns)],
            'summary': entry.find('a:summary', ns).text.strip().replace('\n', ' '),
            'categories': [c.attrib.get('term', '') for c in entry.findall('a:category', ns)],
            'pdf': next((link.attrib['href'] for link in entry.findall('a:link', ns)
                        if link.attrib.get('title') == 'pdf'), None),
            'published': entry.find('a:published', ns).text.strip(),
        })
    return papers

def extract_algorithm_from_paper(arxiv_id: str):
    """
    Fetch paper HTML/PDF, extract algorithm pseudocode.
    Returns structured algorithm description (if accessible).
    Falls back to abstract + potential method keywords.
    """
    # Implementation depends on paper format;
    # for arXiv HTML abstracts, scrape and keyword-extract.
    pass
```

### Workflow for Implementing a New Algorithm from arXiv
```
1. Search: papers = search_arxiv("adaptive optimization transformer", categories=["cs.LG", "stat.ML"])
2. Read: for each paper, read title, abstract, identify algorithmic contribution
3. Extract: identify key steps / pseudocode from the paper
4. Implement: use the code templates above as skeleton
5. Benchmark: compare against AdamW, SGD+momentum on standard tasks
6. Report: convergence curves, final loss, wall-clock time
```


## Benchmarking (Reproducible)

### Protocol
1. **Seed**: fix `np.random.seed(seed)` and `torch.manual_seed(seed)` for reproducibility
2. **Multiple runs**: ≥5 independent runs with different seeds
3. **Metrics**: final objective value (mean ± std), convergence rate (time to threshold), wall-clock time
4. **Comparison**: include baseline algorithms (standard implementations from `scipy.optimize`, `torch.optim`)
5. **Reporting**: table with mean ± std, convergence plot, Pareto frontier of time vs accuracy

### Convergence Diagnostics
```python
def convergence_diagnostics(history, true_opt=None, log_scale=True):
    """
    Plot convergence: f(x_k) vs iteration.
    If true_opt known, plot suboptimality f(x_k) - f*.
    """
    import matplotlib.pyplot as plt
    if true_opt is not None:
        history = np.array(history) - true_opt
    plt.figure(figsize=(8, 5))
    plt.plot(history)
    if log_scale and np.all(history > 0):
        plt.yscale('log')
    plt.xlabel('Iteration')
    plt.ylabel('Suboptimality' if true_opt else 'Objective')
    plt.grid(True, alpha=0.3)
    plt.show()
```


## Key References

### Foundational
- Boyd & Vandenberghe, *Convex Optimization* (2004) — https://web.stanford.edu/~boyd/cvxbook/
- Nocedal & Wright, *Numerical Optimization* (2nd ed, 2006)
- Bertsekas, *Nonlinear Programming* (3rd ed, 2016)
- Goodfellow, Bengio, Courville, *Deep Learning* (2016) — Chapter 8: Optimization

### Algorithm-Specific
- Robbins & Monro, "A Stochastic Approximation Method" (1951) — *Annals of Mathematical Statistics*
- Kingma & Ba, "Adam: A Method for Stochastic Optimization" (2015) — ICLR
- Loshchilov & Hutter, "Decoupled Weight Decay Regularization" (2019) — ICLR
- Duchi, Hazan, Singer, "Adaptive Subgradient Methods" (2011) — JMLR
- Nesterov, "A method for solving a convex programming problem..." (1983) — *Soviet Math. Dokl.*
- Tieleman & Hinton, "RMSProp" (2012) — Coursera lecture
- Dempster, Laird, Rubin, "Maximum Likelihood from Incomplete Data via the EM Algorithm" (1977) — *JRSS-B*
- Neal, "MCMC using Hamiltonian dynamics" (2011) — *Handbook of MCMC*
- Hoffman & Gelman, "The No-U-Turn Sampler" (2014) — JMLR

### Recent Advances (2023-2025)
- Liu et al., "Sophia: A Scalable Stochastic Second-order Optimizer..." (2024) — arXiv:2305.14342
- Gupta et al., "Shampoo: Preconditioned SGD..." (2018) — ICML
- Zhang et al., "AdaBelief Optimizer" (2020) — NeurIPS
- Chen et al., "Symbolic Discovery of Optimization Algorithms" (2024) — arXiv:2302.06675
- Deng et al., "GaLore: Memory-Efficient LLM Training..." (2024) — arXiv:2403.03507


## Quick-Start Checklist
1. `pip install numpy scipy cvxpy pulp torch pymc deap matplotlib`
2. Determine problem class (LP, convex, stochastic, combinatorial)
3. Select initial algorithm from the taxonomy above
4. Implement using templates → benchmark → iterate
5. For novel research: `search_arxiv(...)` to find latest, then implement from paper

*This skill provides a rigorous framework for optimization algorithm research and development.*

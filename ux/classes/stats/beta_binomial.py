from matplotlib.axes import Axes
from math import lgamma
from numba import jit
from numpy import linspace, ndarray, tile, tril, exp
from pandas import Series, Index
from scipy.special import comb
from scipy.stats import beta as beta_sp

from ux.plots.helpers import new_axes


class BetaBinomial(object):
    """
    Class for calculating Bayesian probabilities using the Beta Binomial distribution.

    Prior Hyper-parameters
    ----------------------
    * `α` and `β` are the hyper-parameters of the prior.
    * `α > 0`
    * `β > 0`
    * Interpretation is α-1 successes and β-1 failures.

    Posterior Hyper-parameters
    --------------------------
    * `n` is the number of trials.
    * `m` is the number of successes over `n` trials.

    Model parameters
    ----------------
    * `θ` is the probability of a successful trial.
    * `0 ≤ θ ≤ 1`

    Links
    -----
    * https://en.wikipedia.org/wiki/Beta_distribution
    * https://en.wikipedia.org/wiki/Binomial_distribution
    * https://en.wikipedia.org/wiki/Beta-binomial_distribution
    * https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_discrete_distribution
    """
    def __init__(self, alpha: int = 1, beta: int = 1, n: int = 0, m: int = 0, theta: ndarray = None):
        """
        Create a new beta-binomial model using the parameters of the prior beta distribution.

        :param alpha: value of α for the prior distribution
        :param beta: value of β for the prior distribution
        :param n: number of trials
        :param m: number of successes
        :param theta: values to define probability distribution at - controls granularity
        """
        self.alpha = alpha
        self.beta = beta
        self.theta = theta or linspace(0, 1, 10001)
        self.n = n
        self.m = m

    def prior(self, theta: ndarray = None):
        """
        Return the prior probability of the parameter θ given the priors α, β

        `p(θ|α,β)`

        :param theta: vector of possible `θ`s
        :rtype: Series
        """
        theta = theta or self.theta
        return Series(
            data=beta_sp(self.alpha, self.beta).pdf(theta),
            index=Index(data=theta, name='θ'),
            name='p(θ|α={},β={})'.format(self.alpha, self.beta)
        )

    def likelihood(self, theta=None, n: int = None, m: int = None):
        """
        Return the likelihood of observing the data n, m given the parameters θ.
        N.B. does not include normalization constant so posterior != prior * likelihood.

        `p(m|n,θ)`

        :param theta: vector of possible `θ`s
        :param n: number of trials (use instance value if not given)
        :param m: number of successes (use instance value if not given)
        :rtype: Series
        """
        theta = theta or self.theta
        n = n or self.n
        m = m or self.m

        return Series(
            data=comb(n, m) * theta ** m * (1 - theta) ** (n - m),
            index=Index(data=theta, name='θ'),
            name='p(m={}|n={},θ)'.format(m, n)
        )

    def posterior(self, theta=None, n: int = None, m: int = None):
        """
        Return the posterior probability of the parameters given the data n, m and priors α,β

        `p(θ|n,m,α,β)`

        :param theta: vector of possible `θ`s
        :param n: number of trials (use instance value if not given)
        :param m: number of successes (use instance value if not given)
        :rtype: Series
        """
        theta = theta if theta is not None else self.theta
        n = n or self.n
        m = m or self.m
        return Series(
            data=beta_sp(self.alpha + m, self.beta + n - m).pdf(theta),
            index=Index(data=theta, name='θ'),
            name='p(θ|n={},m={},α={},β={})'.format(n, m, self.alpha, self.beta)
        )

    def posterior_hpd(self, percent: float = 0.94, n: int = None, m: int = None):
        """
        Return the bounds of the highest posterior density region of the posterior distribution.

        `p(θ|n,m,α,β)`

        :param percent: percentage for the HPD
        :param n: number of trials (use instance value if not given)
        :param m: number of successes (use instance value if not given)
        :rtype: float, float
        """
        n = n or self.n
        m = m or self.m
        dist = beta_sp(self.alpha + m, self.beta + n - m)
        return dist.interval(percent)

    def posterior_mean(self, n: int = None, m: int = None):
        """
        Return the mean of the posterior distribution.

        :param n: number of trials (use instance value if not given)
        :param m: number of successes (use instance value if not given)
        :rtype: float
        """
        n = n or self.n
        m = m or self.m
        dist = beta_sp(self.alpha + m, self.beta + n - m)
        return dist.mean()

    def plot_prior(self, theta=None, color: str = None, ax: Axes = None):
        """
        Plot the prior probability of the parameter θ given the priors α, β

        `p(θ|α,β)`

        :param theta: vector of possible `θ`s
        :param color: Optional color for the series.
        :param ax: Optional matplotlib axes
        :rtype: Axes
        """
        ax = ax or new_axes()
        theta = theta or self.theta
        prior = self.prior(theta=theta)
        prior.plot(kind='line', label='α={}, β={}'.format(self.alpha, self.beta),
                   color=color or 'C0', ax=ax)
        ax.set_xlabel('θ')
        ax.set_ylabel('p(θ|α,β)')
        ax.legend()
        return ax

    def plot_likelihood(self, theta: ndarray = None, n: int = None, m: int = None, color: str = None, ax: Axes = None):
        """
        Return the likelihood of observing the data n, m given the parameters θ

        `p(m|n,θ)`

        :param theta: vector of possible `θ`s
        :param n: number of trials (use instance value if not given)
        :param m: number of successes (use instance value if not given)
        :param color: Optional color for the series.
        :param ax: Optional matplotlib axes
        :rtype: Axes
        """
        ax = ax or new_axes()
        n = n or self.n
        m = m or self.m
        likelihood = self.likelihood(theta=theta, n=n, m=m)
        likelihood.plot(kind='line', label='n={}, m={}'.format(n, m),
                        color=color or 'C1', ax=ax)
        ax.set_xlabel('θ')
        ax.set_ylabel('p(m|n,θ)')
        ax.legend()
        return ax

    def plot_posterior(self, theta: ndarray = None,
                       n: int = None, m: int = None,
                       ndp: int = 2,
                       hpd_width: float = 0.94, hpd_y: float = None, hpd_color: str = 'k',
                       label: str = None, color: str = None,
                       ax: Axes = None):
        """
        Return the posterior probability of the parameters given the data n, m and priors α, β

        `p(θ|n,m,α,β)`

        :param theta: vector of possible `θ`s
        :param n: number of trials (use instance value if not given)
        :param m: m number of successes (use instance value if not given)
        :param hpd_width: Width of the Highest Posterior Density region to plot (0 to 1). Defaults to 0.94
        :param hpd_y: Manual override of the y-coordinate for the HPD line. Defaults to posterior max / 10
        :param ndp: Number of decimal places to round the labels for the upper and lower bounds of the HPD and the mean.
        :param hpd_color: Color for the HPD line.
        :param label: Optional series label to override the default.
        :param color: Optional color for the series.
        :param ax: Optional matplotlib axes
        :rtype: Axes
        """
        ax = ax or new_axes()
        theta = theta if theta is not None else self.theta
        n = n or self.n
        m = m or self.m
        posterior = self.posterior(theta=theta, n=n, m=m)
        # plot distribution
        label = label or 'α={}, β={}, n={}, m={}'.format(self.alpha, self.beta, n, m)
        ax = posterior.plot(kind='line', label=label, color=color or 'C2', ax=ax)
        # plot posterior_hpd
        hpd_low, hpd_high = self.posterior_hpd(percent=hpd_width, n=n, m=m)
        hpd_y = hpd_y if hpd_y is not None else posterior.max() / 10
        ax.plot((hpd_low, hpd_high), (hpd_y, hpd_y), color=hpd_color)
        ax.text(hpd_low, hpd_y, str(round(hpd_low, ndp)), ha='right', va='top')
        ax.text(hpd_high, hpd_y, str(round(hpd_high, ndp)), ha='left', va='top')
        ax.text((hpd_low + hpd_high) / 2, posterior.max() * 0.5,
                '{:.0f}% HPD'.format(hpd_width * 100), ha='center', va='bottom')
        # plot mean
        mean = self.posterior_mean(n=n, m=m)
        ax.text(mean, posterior.max() * 0.95, 'mean = {:.2f}'.format(mean), ha='center')
        # labels
        ax.set_xlabel('θ')
        ax.set_ylabel('p(θ|n,m,α,β)')
        ax.legend()
        return ax

    def prob_posterior_greater(self, other, method: str = 'exact', n_samples: int = None):
        """
        Return the approximate probability that a random value of the posterior density is greater
        than that of another distribution.
        N.B. this method only produces and approximate solution and is slow due to the requirement to
        calculate the square matrix. Sampling from each distribution is much faster and more accurate.
        Use a closed form solution wherever possible.

        :type other: BetaBinomial
        :param method: One of ['exact', 'sample', 'approx']
        :param n_samples: Only used for 'sample' and 'approx' methods. Defaults to sensible values for each method.
        :rtype: float
        """
        if method == 'exact':
            @jit
            def h(a, b, c, d):
                num = lgamma(a + c) + lgamma(b + d) + lgamma(a + b) + lgamma(c + d)
                den = lgamma(a) + lgamma(b) + lgamma(c) + lgamma(d) + lgamma(a + b + c + d)
                return exp(num - den)

            @jit
            def g0(a, b, c):
                return exp(lgamma(a + b) + lgamma(a + c) - (lgamma(a + b + c) + lgamma(a)))

            @jit
            def hiter(a, b, c, d):
                while d > 1:
                    d -= 1
                    yield h(a, b, c, d) / d

            @jit
            def g(a, b, c, d):
                return g0(a, b, c) + sum(hiter(a, b, c, d))

            return g(a=self.alpha + self.m, b=self.beta + self.n - self.m,
                     c=other.alpha + other.m, d=other.beta + other.n - other.m)

        elif method == 'samples':
            n_samples = n_samples or 100001
            self_samples = beta_sp(self.alpha + self.m, self.beta + self.n - self.m).rvs(n_samples)
            other_samples = beta_sp(other.alpha + other.m, other.beta + other.n - other.m).rvs(n_samples)
            return sum(self_samples > other_samples) / n_samples
        elif method == 'approx':
            n_steps = n_samples or 10001
            # get PDFs
            pdf_self = self.posterior(theta=self.theta)
            pdf_other = other.posterior(theta=self.theta)
            # tile each pdf in orthogonal directions and multiply probabilities
            n_steps = len(self.theta)
            a_self = tile(pdf_self.values, (n_steps, 1)).T
            a_other = tile(pdf_other.values, (n_steps, 1))
            a_prod = a_self * a_other
            # sum p1(θ1) * p2(θ2) in lower triangle (excluding diagonal) i.e. where θ1 > θ2, and normalize
            p_total = tril(a_prod, k=1).sum() / a_prod.sum()
            return p_total

    def prob_ppd_superior(self, other, method: str='samples', n_samples: int = None):
        """
        Return the approximate probability that a random value of the posterior predictive distribution
        is greater than that of another distribution.

        :type other: BetaBinomial
        :rtype: float
        """
        if method == 'samples':
            n_samples = n_samples or 100001
            self_samples = beta_sp(self.alpha + self.m, self.beta + self.n - self.m).rvs(n_samples)
            other_samples = beta_sp(other.alpha + other.m, other.beta + other.n - other.m).rvs(n_samples)
            return sum(self_samples * (1 - other_samples)) / n_samples
        elif method == 'approx':
            # get PDFs
            p_theta_1 = self.posterior(theta=self.theta)
            p_theta_2 = other.posterior(theta=self.theta)
            # tile each pdf in orthogonal directions and multiply probabilities
            n_steps = len(self.theta)
            g_theta_1 = tile(p_theta_1.values, (n_steps, 1)).T
            g_theta_2 = tile(p_theta_2.values, (n_steps, 1))
            p_y1 = tile(p_theta_1.index, (n_steps, 1)).T
            p_y2 = tile(p_theta_2.index, (n_steps, 1))
            p_t1_t2 = g_theta_1 * g_theta_2
            p_y1_is_1_y2_is_0 = (p_t1_t2 * p_y1 * (1 - p_y2)).sum() / p_t1_t2.sum()
            return p_y1_is_1_y2_is_0

    def __repr__(self):

        return 'BetaBinomial(α={}, β={}, n={}, m={})'.format(
            self.alpha, self.beta, self.n, self.m
        )

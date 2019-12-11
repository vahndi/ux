from matplotlib.axes import Axes
from numpy import linspace, ndarray, tile, tril
from pandas import Series, Index
from scipy.stats import gamma

from ux.plots.helpers import new_axes


class GammaExponential(object):
    """
    Class for calculating Bayesian probabilities using the Gamma Exponential distribution.

    Prior Hyper-parameters
    ----------------------
    * `α` and `β` OR `k` and `θ` are the hyper-parameters of the prior.
    * `k` and `α` are the same parameter, i.e. the shape parameter.
    * `θ` is the scale parameter.
    * `β` is the rate or inverse-scale parameter. `β = 1 / θ`
    * `a > 0` and can be interpreted as the number of prior observations.
    * `β > 0` and can be interpreted as the total time for prior observations.
    * `k > 0`
    * `θ > 0`

    Posterior Hyper-parameters
    --------------------------
    * `n` is the number of observations
    * `x̄` is the average time between observations

    Model parameters
    ----------------
    * `λ` is the rate of the exponential distribution `P(x) = λ·exp(-λx)`
    * `0 < λ`

    Links
    -----
    * https://en.wikipedia.org/wiki/Gamma_distribution
    * https://en.wikipedia.org/wiki/Exponential_distribution
    * https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_continuous_distribution
    """
    def __init__(self, alpha: float = 0.001, beta: float = 0.001,
                 k: float = None, theta: float = None,
                 n: int = 0, x_mean: float = 0.0,
                 lambda_: ndarray = None):
        """
        Create a new gamma-exponential model using the parameters of the prior gamma distribution.

        :param alpha: Scale parameter when providing the rate parameter.
        :param beta: Rate parameter.
        :param k: Scale parameter when providing the scale parameter.
        :param theta: Scale parameter. Inverse of rate parameter.
        :param lambda_: Values to define probability distribution at - controls granularity
        """
        self.alpha = None
        self.beta = None
        self._parametrization = None
        if None not in (alpha, beta) and k is None and theta is None:
            self.alpha = alpha
            self.beta = beta
            self._parametrization = 'ab'
        elif None not in (k, theta) and alpha is None and beta is None:
            self.alpha = k
            self.beta = 1 / theta
            self._parametrization = 'kt'
        else:
            raise ValueError('Either provide α and β or k and θ')
        self.n = n
        self.x_mean = x_mean
        self.lambda_ = lambda_ if lambda_ is not None else linspace(0, 10, 10001)

    def prior(self, lambda_: ndarray = None):
        """
        Return the prior probability of the parameter θ given the priors α, β

        `p(x|α,β)`

        :param lambda_: vector of possible `λ`s
        :rtype: Series
        """
        lambda_ = lambda_ or self.lambda_
        if self._parametrization == 'ab':
            name = 'p(λ|α={},β={})'.format(self.alpha, self.beta)
        else:
            name = 'p(λ|k={},θ={})'.format(self.alpha, 1 / self.beta)
        return Series(
            data=gamma(a=self.alpha, scale=1 / self.beta).pdf(lambda_),
            index=Index(data=lambda_, name='λ'), name=name
        )

    def posterior(self, lambda_: ndarray = None, n: int = None, x_mean: float = None):
        """
        Return the posterior probability of the parameters given the data n, x̄ and priors α,β

        `p(λ|n,x̄,α,β)`

        :param lambda_: vector of possible `λ`s
        :param n: number of observations
        :param x_mean: average time between observations
        :rtype: Series
        """
        lambda_ = lambda_ if lambda_ is not None else self.lambda_
        n = n or self.n
        x_mean = x_mean or self.x_mean
        if self._parametrization == 'ab':
            name = 'p(λ|n={},x̄={},α={},β={})'.format(n, x_mean, self.alpha, self.beta)
        else:
            name = 'p(λ|n={},x̄={},k={},θ={})'.format(n, x_mean, self.alpha, 1 / self.beta)
        return Series(
            data=gamma(a=self.alpha + n, scale=1 / (self.beta + n * x_mean)).pdf(lambda_),
            index=Index(data=lambda_, name='λ'), name=name
        )

    def posterior_hpd(self, percent: float = 0.94, n: int = None, x_mean: float = None):
        """
        Return the bounds of the highest posterior density region of the posterior distribution.

        `p(λ|n,x̄,α,β)`

        :param percent: percentage for the HPD
        :param n: number of observations
        :param x_mean: average time between observations
        :rtype: float, float
        """
        n = n or self.n
        x_mean = x_mean or self.x_mean
        dist = gamma(a=self.alpha + n, scale=1 / (self.beta + n * x_mean))
        return dist.interval(percent)

    def posterior_mean(self, n: int = None, x_mean: float = None):
        """
        Return the mean of the posterior distribution.

        :param n: number of observations
        :param x_mean: average time between observations
        :rtype: float
        """
        n = n or self.n
        x_mean = x_mean or self.x_mean
        dist = gamma(a=self.alpha + n, scale=1 / (self.beta + n * x_mean))
        return dist.mean()

    def plot_prior(self, lambda_: ndarray = None, color: str = None, ax: Axes = None):
        """
        Plot the prior probability of the parameter θ given the priors α, β

        `p(λ|α,β)`

        :param lambda_: vector of possible `λ`s
        :param color: Optional color for the series.
        :param ax: Optional matplotlib axes
        :rtype: Axes
        """
        ax = ax or new_axes()
        prior = self.prior(lambda_=lambda_)
        prior.plot(kind='line', label='α={}, β={}'.format(self.alpha, self.beta),
                   color=color or 'C0', ax=ax)
        ax.set_xlabel('λ')
        if self._parametrization == 'ab':
            y_label = 'p(λ|α,β)'
        else:
            y_label = 'p(λ|k,θ)'
        ax.set_ylabel(y_label)
        ax.legend()
        return ax

    def plot_posterior(self, lambda_: ndarray = None,
                       n: int = None, x_mean: float = None,
                       ndp: int = 2,
                       hpd_width: float = 0.94, hpd_y: float = None, hpd_color: str = 'k',
                       label: str = None, color: str = None,
                       ax: Axes = None):
        """
        Return the posterior probability of the parameters given the data n, m and priors α, β

        `p(λ|n,x̄,α,β)`

        :param lambda_: vector of possible `θ`s
        :param n: number of observations
        :param x_mean: average time between observations
        :param ndp: Number of decimal places to round the labels for the upper and lower bounds of the HPD and the mean.
        :param hpd_width: Width of the Highest Posterior Density region to plot (0 to 1). Defaults to 0.94
        :param hpd_y: Manual override of the y-coordinate for the HPD line. Defaults to posterior max / 10
        :param hpd_color: Color for the HPD line.
        :param label: Optional series label to override the default.
        :param color: Optional color for the series.
        :param ax: Optional matplotlib axes
        :rtype: Axes
        """
        ax = ax or new_axes()
        lambda_ = lambda_ if lambda_ is not None else self.lambda_
        n = n or self.n
        x_mean = x_mean or self.x_mean
        posterior = self.posterior(lambda_=lambda_, n=n, x_mean=x_mean)
        # plot distribution
        if self._parametrization == 'ab':
            label = label or 'α={}, β={}, n={}, x̄={}'.format(self.alpha, self.beta, n, x_mean)
        else:
            label = label or 'k={}, θ={}, n={}, x̄={}'.format(self.alpha, 1 / self.beta, n, x_mean)
        ax = posterior.plot(kind='line', label=label, color=color or 'C2', ax=ax)
        # plot posterior_hpd
        hpd_low, hpd_high = self.posterior_hpd(percent=hpd_width, n=n, x_mean=x_mean)
        hpd_y = hpd_y if hpd_y is not None else posterior.max() / 10
        ax.plot((hpd_low, hpd_high), (hpd_y, hpd_y), color=hpd_color)
        ax.text(hpd_low, hpd_y, str(round(hpd_low, ndp)), ha='right', va='top')
        ax.text(hpd_high, hpd_y, str(round(hpd_high, ndp)), ha='left', va='top')
        ax.text((hpd_low + hpd_high) / 2, posterior.max() * 0.5,
                '{:.0f}% HPD'.format(hpd_width * 100), ha='center', va='bottom')
        # plot mean
        mean = self.posterior_mean(n=n, x_mean=x_mean)
        ax.text(mean, posterior.max() * 0.95, 'mean = {}'.format(str(round(mean, ndp))), ha='center')
        # labels
        ax.set_xlabel('λ')
        if self._parametrization == 'ab':
            ax.set_ylabel('p(λ|n,x̄,α,β)')
        else:
            ax.set_ylabel('p(λ|n,x̄,k,θ)')
        ax.legend()
        return ax

    def prob_posterior_greater(self, other, method: str = 'samples', n_samples: int = None):
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
        if method == 'samples':
            n_samples = n_samples or 100001
            self_samples = gamma(a=self.alpha + self.n, scale=1 / (self.beta + self.n * self.x_mean)).rvs(n_samples)
            other_samples = gamma(a=other.alpha + other.n, scale=1 / (other.beta + other.n * other.x_mean)).rvs(n_samples)
            return sum(self_samples > other_samples) / n_samples
        elif method == 'approx':
            n_steps = n_samples or 10001
            # get PDFs
            pdf_self = self.posterior(lambda_=self.lambda_)
            pdf_other = other.posterior(lambda_=self.lambda_)
            # tile each pdf in orthogonal directions and multiply probabilities
            n_steps = len(self.lambda_)
            a_self = tile(pdf_self.values, (n_steps, 1)).T
            a_other = tile(pdf_other.values, (n_steps, 1))
            a_prod = a_self * a_other
            # sum p1(θ1) * p2(θ2) in lower triangle (excluding diagonal) i.e. where θ1 > θ2, and normalize
            p_total = tril(a_prod, k=1).sum() / a_prod.sum()
            return p_total


def plot_wikipedia():

    import matplotlib.pyplot as plt
    ax = new_axes()
    for k, t, c in [
        (1, 2, 'red'),
        (2, 2, 'orange'),
        (3, 2, 'yellow'),
        (5, 1, 'green'),
        (9, 0.5, 'black'),
        (7.5, 1, 'blue'),
        (0.5, 1, 'purple'),
        (0.1, 0.1, 'pink'),
    ]:
        ge = GammaExponential(k=k, theta=t)
        ge.plot_prior(ax=ax, color=c)
    ax.set_ylim(0, 0.5)
    ax.set_title('https://en.wikipedia.org/wiki/Gamma_distribution#/media/File:Gamma_distribution_pdf.svg')
    plt.show()


if __name__ == '__main__':

    ge = GammaExponential(alpha=1, beta=1, n=50, x_mean=2)
    print(ge.posterior_mean())

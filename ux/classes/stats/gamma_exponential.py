from matplotlib.axes import Axes
from numpy import linspace, ndarray
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

    Support
    -------


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
        self.lambda_ = lambda_ or linspace(0, 20, 10001)

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

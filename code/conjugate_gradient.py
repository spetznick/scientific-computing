
import numpy as np
import scipy.linalg as la


def create_discretized_diffusion_equation_matrix(size=10, c=0.1):
    h = 1/size
    A = (2 + h**2 * c) * np.identity(size)
    for i in range(1, size):
        A[i][i-1] = -1
        A[i-1][i] = -1
    return A


def create_restriction_matrix(size):
    d = np.ones(size)
    d_low = 2*np.ones()
    return np.diag(d,)(size, size//2, k=2, )


def create_coarsening_matrix(h):
    """
    Create a coarsening matrix for a given finer grid size h.

    Parameters:
    - h: Size of the finer grid.

    Returns:
    - A numpy matrix representing the coarsening matrix.
    """
    if h % 2 != 0:
        raise ValueError("The size of the finer grid 'h' should be even.")
    size_fine = h+1
    size_coarse = size_fine // 2

    coarsening_matrix = np.zeros((size_coarse, size_fine))

    # Fill the diagonal with ones
    coarsening_matrix[np.arange(size_coarse),
                      np.arange(0, size_fine - 2, 2)] = 1

    # Fill the upper diagonal with twos
    coarsening_matrix[np.arange(size_coarse),
                      np.arange(1, size_fine - 1, 2)] = 2

    # Fill the second upper diagonal with ones
    coarsening_matrix[np.arange(size_coarse),
                      np.arange(2, size_fine, 2)] = 1

    return coarsening_matrix/4


def create_prolongation_matrix(h):
    """
    Uses `create_coarsening_matrix` and returns the transpose of the matrix
    multiplied by 2
    """
    return 2 * np.transpose(create_coarsening_matrix(h))


def u_sol(x): return np.exp(x)*(1-x)


def f_rhs(c, x): return np.exp(x)*(c-1-c*x-x)


def conjugate_gradient_with_ritz(A, b, max_iter=100, tol=1e-8):
    """
    Conjugate Gradient algorithm with Ritz value computation for a one-dimensional problem.

    Parameters:
    - A: Symmetric positive definite matrix (1D array representing the diagonal elements).
    - b: Right-hand side vector.
    - max_iter: Maximum number of iterations.
    - tol: Tolerance for convergence.

    Returns:
    - x: Solution vector.
    - ritz_values: List of Ritz values computed at each iteration.
    """

    n = len(b)
    x = np.zeros(n)  # Initial guess
    r = b - np.diag(A) * x
    p = r.copy()
    r_norm = np.linalg.norm(r, ord=2)
    T_k = np.array(r_norm)
    ritz_values = []

    for k in range(max_iter):
        Ap = np.diag(A) * p
        alpha = np.dot(r, r) / np.dot(p, Ap)
        x = x + alpha * p
        r_new = r - alpha * Ap

        # Compute the Ritz value
        ritz_value = np.dot(r_new, r_new) / np.dot(r, r)
        ritz_values.append(ritz_value)

        if np.linalg.norm(r_new) < tol:
            break

        beta = np.dot(r_new, r_new) / np.dot(r, r)
        p = r_new + beta * p
        r = r_new

    return x, ritz_values


def return_boundary_values():
    alpha = 1
    beta = 0
    return alpha, beta


if __name__ == "__main__":
    # Example usage:
    A = create_discretized_diffusion_equation_matrix(2)

    A = np.diag(np.linspace(1, 5, 10))  # Symmetric positive definite matrix
    b = np.ones(10)  # Right-hand side vector

    # solution, ritz_values = conjugate_gradient_with_ritz(A, b)

    # Print the solution and Ritz values
    # print("Solution:", solution)
    # print("Ritz Values:", ritz_values)

    # Example usage:
    h = 8
    coarsening_matrix = create_coarsening_matrix(h)
    print("Coarsening Matrix:")
    print(4*coarsening_matrix)
    prolongation_matrix = create_prolongation_matrix(h)
    print("Prolongation Matrix:")
    print(2*prolongation_matrix)

from typing import Callable, Dict, List, Literal, Optional, Type, Union

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from devinterp.optim.sgld import SGLD
from devinterp.slt.sampler import sample


def estimate_learning_coeff(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: Callable,
    sampling_method: Type[torch.optim.Optimizer] = SGLD,
    optimizer_kwargs: Optional[Dict[str, Union[float, Literal["adaptive"]]]] = None,
    num_draws: int = 100,
    num_chains: int = 10,
    num_burnin_steps: int = 0,
    num_steps_bw_draws: int = 1,
    clip_chains_quantile: float|None = None,
    cores: int = 1,
    seed: Optional[Union[int, List[int]]] = None,
    pbar: bool = True,
    device: torch.device = torch.device("cpu"),
    verbose: bool = True,
) -> float:
    trace = sample(
        model=model,
        loader=loader,
        criterion=criterion,
        sampling_method=sampling_method,
        optimizer_kwargs=optimizer_kwargs,
        num_draws=num_draws,
        num_chains=num_chains,
        num_burnin_steps=num_burnin_steps,
        num_steps_bw_draws=num_steps_bw_draws,
        cores=cores,
        seed=seed,
        pbar=pbar,
        device=device,
        verbose=verbose,
    )
    baseline_loss = trace.loc[trace["chain"] == 0, "loss"].iloc[0]
    if clip_chains_quantile is not None:
        trace = chain_clipper(trace, clip_chains_quantile)
    avg_loss = trace.groupby("chain")["loss"].mean().mean()
    num_samples = len(loader.dataset)

    return (avg_loss - baseline_loss) * num_samples / np.log(num_samples)

def chain_clipper(trace: pd.DataFrame, q:float=0.95) -> pd.DataFrame:

    def group_clip(group, q=0.9):
        q_value = group["loss"].quantile(q)
        #group.loc[:, "loss_capped"] = group["loss"].copy()
        group.loc[group["loss"] >= q_value, "loss"] = q_value
        return group
    
    return trace.groupby("chain",group_keys=False).apply(group_clip,q=q)
    

def estimate_learning_coeff_with_summary(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: Callable,
    sampling_method: Type[torch.optim.Optimizer] = SGLD,
    optimizer_kwargs: Optional[Dict[str, Union[float, Literal["adaptive"]]]] = None,
    num_draws: int = 100,
    num_chains: int = 10,
    num_burnin_steps: int = 0,
    num_steps_bw_draws: int = 1,
    clip_chains_quantile: float|None = None,
    cores: int = 1,
    seed: Optional[Union[int, List[int]]] = None,
    pbar: bool = True,
    device: torch.device = torch.device("cpu"),
    verbose: bool = True,
) -> dict:
    trace = sample(
        model=model,
        loader=loader,
        criterion=criterion,
        sampling_method=sampling_method,
        optimizer_kwargs=optimizer_kwargs,
        num_draws=num_draws,
        num_chains=num_chains,
        num_burnin_steps=num_burnin_steps,
        num_steps_bw_draws=num_steps_bw_draws,
        cores=cores,
        seed=seed,
        pbar=pbar,
        device=device,
        verbose=verbose,
    )

    baseline_loss = trace.loc[trace["chain"] == 0, "loss"].iloc[0]
    num_samples = len(loader.dataset)

    if clip_chains_quantile is not None:
        trace = chain_clipper(trace, clip_chains_quantile)
    avg_losses = trace.groupby("chain")["loss"].mean()
    results = torch.zeros(num_chains, device=device)

    for i in range(num_chains):
        chain_avg_loss = avg_losses.iloc[i]
        results[i] = (chain_avg_loss - baseline_loss) * num_samples / np.log(num_samples)

    avg_loss = results.mean()
    std_loss = results.std()

    return {
        "mean": avg_loss.item(),
        "std": std_loss.item(),
        **{f"chain_{i}": results[i].item() for i in range(num_chains)},
        "trace": trace,
    }


def plot_learning_coeff_trace(trace: pd.DataFrame, **kwargs):
    import matplotlib.pyplot as plt

    for chain, df in trace.groupby("chain"):
        plt.plot(df["step"], df["loss"], label=f"Chain {chain}", **kwargs)

    plt.xlabel("Step")
    plt.ylabel(r"$L_n(w)$")
    plt.title("Learning Coefficient Trace")
    plt.legend()
    plt.show()

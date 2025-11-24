# Simulation Settings

Documentation of the simulation settings used to run the model.

## Time

### Initial Time

- **Value:** `0`
- **Units:** `month`
- **Description:** Starting point of simulation.

### Final Time

- **Value:** `120`
- **Units:** `month`
- **Description:** Length of simulation (10 years). This length aligns with timeframes of proven methodologies for analyzing carbon tax [[1]](#ref1).

### Time Step

- **Value:** `1`
- **Units:** `month`
- **Description:** The time step for the simulation.

### Saveper

- **Value:** `1`
- **Units:** `month`
- **Description:** Frequency at which output data is saved.

## Integration Method

Euler integration is used for stock updates.

## Control Parameter

Carbon tax rate.

## References

<a name="ref1"></a>[1] Horowitz, J., et al. (2017). Methodology for Analyzing a Carbon Tax. [Link](https://home.treasury.gov/system/files/131/WP-115.pdf)

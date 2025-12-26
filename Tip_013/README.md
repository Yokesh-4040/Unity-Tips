# #UNITY TIPS 013/100

## Generating Random Points on Circles and Spheres

<img src="Tip0013.png" alt="Random Points on Circles and Spheres" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

When spawning particles, positioning enemies, or creating procedural effects, you often need random points distributed on or within circles and spheres. Unity's `Random.insideUnitCircle` and `Random.onUnitSphere` provide efficient, uniform distribution, but there's a critical detail many developers overlook: proper normalization and scaling.

Understanding the difference between points *inside* a circle versus *on* a circle's circumference—and how to properly scale these values—is essential for creating natural-looking randomization in your games. This tip explores the mathematical foundations and practical applications of circular and spherical randomization.

<br clear="left">

## The Problem

Generating random points with uniform distribution isn't as simple as randomizing X and Y coordinates independently. Naive approaches like `new Vector2(Random.Range(-1, 1), Random.Range(-1, 1))` create square distributions, not circular ones. This results in clustering at corners and non-uniform density.

For circles, you need points either:
- **Inside** the circle (filled disc) - like particle spawn areas
- **On** the circle's edge (circumference) - like orbital positions

For spheres, similar needs arise in 3D:
- **On** the sphere's surface - like spawn points around a player
- **Inside** the sphere's volume - like explosion debris fields

## The Solution

Unity provides specialized methods that handle the complex mathematics of uniform distribution:

```csharp
// 2D: Random point INSIDE a unit circle (radius 1)
Vector2 pointInCircle = Random.insideUnitCircle;

// 3D: Random point ON a unit sphere's surface (radius 1)
Vector3 pointOnSphere = Random.onUnitSphere;
```

The key is understanding what "unit" means (radius = 1) and how to scale these to your desired radius. For `insideUnitCircle`, you **must normalize before scaling** to get points on the circle's edge.

## Code Examples

### Basic Circle Point Generation

```csharp
using UnityEngine;

public class CircleSpawner : MonoBehaviour
{
    [SerializeField] private float radius = 5f;
    [SerializeField] private GameObject prefab;

    void SpawnInCircle()
    {
        // Random point INSIDE the circle
        Vector2 randomPoint = Random.insideUnitCircle * radius;
        Vector3 spawnPos = new Vector3(randomPoint.x, 0, randomPoint.y);
        Instantiate(prefab, spawnPos, Quaternion.identity);
    }

    void SpawnOnCircle()
    {
        // Random point ON the circle's edge
        // MUST normalize first!
        Vector2 randomDirection = Random.insideUnitCircle.normalized;
        Vector2 randomPoint = randomDirection * radius;
        Vector3 spawnPos = new Vector3(randomPoint.x, 0, randomPoint.y);
        Instantiate(prefab, spawnPos, Quaternion.identity);
    }
}
```

### Basic Sphere Point Generation

```csharp
using UnityEngine;

public class SphereSpawner : MonoBehaviour
{
    [SerializeField] private float radius = 10f;
    [SerializeField] private GameObject prefab;

    void SpawnOnSphere()
    {
        // Random point ON the sphere's surface
        Vector3 randomPoint = Random.onUnitSphere * radius;
        Instantiate(prefab, randomPoint, Quaternion.identity);
    }

    void SpawnInSphere()
    {
        // Random point INSIDE the sphere's volume
        // Scale by random distance to maintain uniform distribution
        Vector3 randomDirection = Random.onUnitSphere;
        float randomDistance = Random.Range(0f, radius);
        Vector3 randomPoint = randomDirection * randomDistance;
        Instantiate(prefab, randomPoint, Quaternion.identity);
    }
}
```

### Particle System with Random Circular Velocity

```csharp
using UnityEngine;

public class CircularParticleEmitter : MonoBehaviour
{
    [SerializeField] private float minSpeed = 2f;
    [SerializeField] private float maxSpeed = 5f;
    [SerializeField] private ParticleSystem particles;

    void Start()
    {
        var main = particles.main;
        main.startSpeed = 0; // We'll set velocity manually

        var emission = particles.emission;
        emission.rateOverTime = 10;
    }

    void Update()
    {
        // For each new particle, set random outward velocity
        ParticleSystem.Particle[] particleArray =
            new ParticleSystem.Particle[particles.particleCount];
        particles.GetParticles(particleArray);

        for (int i = 0; i < particleArray.Length; i++)
        {
            if (particleArray[i].remainingLifetime == particleArray[i].startLifetime)
            {
                // New particle - set random circular velocity
                Vector2 randomDir = Random.insideUnitCircle.normalized;
                float speed = Random.Range(minSpeed, maxSpeed);
                particleArray[i].velocity = new Vector3(
                    randomDir.x * speed,
                    randomDir.y * speed,
                    0
                );
            }
        }

        particles.SetParticles(particleArray);
    }
}
```

### Enemy Spawner Around Player

```csharp
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    [SerializeField] private GameObject enemyPrefab;
    [SerializeField] private Transform player;
    [SerializeField] private float spawnRadius = 15f;
    [SerializeField] private float spawnHeight = 0f;

    public void SpawnEnemyAroundPlayer()
    {
        // Spawn enemy on circle around player
        Vector2 randomDirection = Random.insideUnitCircle.normalized;
        Vector3 spawnOffset = new Vector3(
            randomDirection.x * spawnRadius,
            spawnHeight,
            randomDirection.y * spawnRadius
        );

        Vector3 spawnPosition = player.position + spawnOffset;
        GameObject enemy = Instantiate(enemyPrefab, spawnPosition, Quaternion.identity);

        // Make enemy face the player
        enemy.transform.LookAt(player);
    }
}
```

### Orbital Satellite System

```csharp
using UnityEngine;

public class SatelliteOrbit : MonoBehaviour
{
    [SerializeField] private GameObject satellitePrefab;
    [SerializeField] private int satelliteCount = 8;
    [SerializeField] private float orbitRadius = 5f;
    [SerializeField] private float orbitSpeed = 30f;

    private GameObject[] satellites;

    void Start()
    {
        satellites = new GameObject[satelliteCount];

        for (int i = 0; i < satelliteCount; i++)
        {
            // Random position ON the orbit circle
            Vector2 randomDir = Random.insideUnitCircle.normalized;
            Vector3 position = new Vector3(
                randomDir.x * orbitRadius,
                0,
                randomDir.y * orbitRadius
            );

            satellites[i] = Instantiate(satellitePrefab, position, Quaternion.identity);
            satellites[i].transform.parent = transform;
        }
    }

    void Update()
    {
        // Rotate the parent to orbit all satellites
        transform.Rotate(Vector3.up, orbitSpeed * Time.deltaTime);
    }
}
```

### Explosion Debris with Spherical Distribution

```csharp
using UnityEngine;

public class ExplosionDebris : MonoBehaviour
{
    [SerializeField] private GameObject debrisPrefab;
    [SerializeField] private int debrisCount = 20;
    [SerializeField] private float explosionForce = 10f;
    [SerializeField] private float explosionRadius = 3f;

    public void Explode()
    {
        for (int i = 0; i < debrisCount; i++)
        {
            // Random direction in 3D space
            Vector3 randomDirection = Random.onUnitSphere;

            // Spawn debris at random position within explosion radius
            Vector3 spawnPos = transform.position +
                (randomDirection * Random.Range(0f, explosionRadius * 0.5f));

            GameObject debris = Instantiate(debrisPrefab, spawnPos, Random.rotation);
            Rigidbody rb = debris.GetComponent<Rigidbody>();

            if (rb != null)
            {
                // Apply force in the random direction
                rb.AddForce(randomDirection * explosionForce, ForceMode.Impulse);

                // Add random spin
                rb.AddTorque(Random.onUnitSphere * explosionForce * 0.5f);
            }
        }

        Destroy(gameObject);
    }
}
```

### Procedural Scatter on Terrain

```csharp
using UnityEngine;

public class TerrainScatter : MonoBehaviour
{
    [SerializeField] private GameObject[] foliagePrefabs;
    [SerializeField] private Transform scatterCenter;
    [SerializeField] private float scatterRadius = 50f;
    [SerializeField] private int objectCount = 100;
    [SerializeField] private LayerMask groundLayer;

    void Start()
    {
        ScatterObjects();
    }

    void ScatterObjects()
    {
        for (int i = 0; i < objectCount; i++)
        {
            // Random point in circle
            Vector2 randomPoint2D = Random.insideUnitCircle * scatterRadius;
            Vector3 randomPoint = new Vector3(
                scatterCenter.position.x + randomPoint2D.x,
                scatterCenter.position.y + 100f, // Start high for raycast
                scatterCenter.position.z + randomPoint2D.y
            );

            // Raycast down to find ground
            if (Physics.Raycast(randomPoint, Vector3.down, out RaycastHit hit, 200f, groundLayer))
            {
                GameObject prefab = foliagePrefabs[Random.Range(0, foliagePrefabs.Length)];
                GameObject obj = Instantiate(prefab, hit.point, Quaternion.identity);

                // Align to surface normal
                obj.transform.up = hit.normal;

                // Random rotation around Y
                obj.transform.Rotate(Vector3.up, Random.Range(0f, 360f), Space.World);

                // Random scale variation
                float scale = Random.Range(0.8f, 1.2f);
                obj.transform.localScale = Vector3.one * scale;
            }
        }
    }
}
```

### Shield Visual Effect with Sphere Distribution

```csharp
using UnityEngine;

public class ShieldEffect : MonoBehaviour
{
    [SerializeField] private GameObject impactEffectPrefab;
    [SerializeField] private float shieldRadius = 2f;
    [SerializeField] private int maxImpactPoints = 5;

    private GameObject[] activeImpacts;

    void Start()
    {
        activeImpacts = new GameObject[maxImpactPoints];
    }

    public void OnHit(Vector3 impactDirection)
    {
        // Find nearest point on shield sphere from impact direction
        Vector3 impactPoint = transform.position +
            (impactDirection.normalized * shieldRadius);

        // Add some randomness around impact point
        Vector3 randomOffset = Random.onUnitSphere * 0.3f;
        Vector3 finalPoint = impactPoint + randomOffset;

        // Project back onto sphere surface
        finalPoint = transform.position +
            ((finalPoint - transform.position).normalized * shieldRadius);

        // Find available slot
        for (int i = 0; i < maxImpactPoints; i++)
        {
            if (activeImpacts[i] == null)
            {
                activeImpacts[i] = Instantiate(impactEffectPrefab, finalPoint, Quaternion.identity);
                activeImpacts[i].transform.parent = transform;
                activeImpacts[i].transform.LookAt(transform.position);
                break;
            }
        }
    }

    public void CreateShieldVisual()
    {
        // Create random points on sphere for shield visualization
        int pointCount = 200;
        for (int i = 0; i < pointCount; i++)
        {
            Vector3 point = transform.position + (Random.onUnitSphere * shieldRadius);
            // Create visual point (particle, line renderer point, etc.)
        }
    }
}
```

## Best Practices

### 1. **Understand the Difference Between Inside and On**
```csharp
// WRONG: Using insideUnitCircle directly for circle edge
Vector2 wrong = Random.insideUnitCircle * radius; // Point could be anywhere inside

// RIGHT: Normalize first for circle edge
Vector2 correct = Random.insideUnitCircle.normalized * radius; // Point on edge
```

### 2. **Always Normalize Before Scaling for Edge Points**
When you want a point **on** the circumference or surface, normalize the random vector first. This ensures the point is exactly at the desired distance.

```csharp
// For circle edge
Vector2 onCircle = Random.insideUnitCircle.normalized * radius;

// For sphere surface (already normalized, but showing principle)
Vector3 onSphere = Random.onUnitSphere * radius;
```

### 3. **Use Appropriate Method for Your Dimensionality**
- 2D games: `Random.insideUnitCircle` (returns Vector2)
- 3D games: `Random.onUnitSphere` (returns Vector3)
- Don't convert unnecessarily between dimensions

### 4. **Handle Zero Vector Edge Case**
`Random.insideUnitCircle` can occasionally return `Vector2.zero`. When normalizing, this becomes `NaN`:

```csharp
Vector2 randomDir = Random.insideUnitCircle;
if (randomDir.sqrMagnitude < 0.0001f) // Check for near-zero
{
    randomDir = Vector2.right; // Fallback direction
}
randomDir.Normalize();
```

### 5. **For Volume Distribution, Scale Distance Correctly**
When distributing points inside a sphere's volume, don't just multiply by random radius—this clusters points at the center:

```csharp
// WRONG: Clusters at center
Vector3 wrong = Random.onUnitSphere * Random.Range(0f, radius);

// BETTER: More uniform, but still not perfect
Vector3 better = Random.onUnitSphere * Mathf.Pow(Random.value, 1f/3f) * radius;

// SIMPLEST: Use Unity's built-in (available in newer versions)
Vector3 best = Random.insideUnitSphere * radius;
```

### 6. **Cache and Reuse Random Directions When Appropriate**
If you need the same random direction multiple times in a frame:

```csharp
Vector3 randomDirection = Random.onUnitSphere; // Calculate once
Vector3 nearPoint = transform.position + randomDirection * nearRadius;
Vector3 farPoint = transform.position + randomDirection * farRadius;
```

### 7. **Consider Performance for Large Batches**
For spawning hundreds of objects, consider batching instantiation and using object pools:

```csharp
// Use object pool
for (int i = 0; i < 1000; i++)
{
    Vector3 pos = Random.onUnitSphere * radius;
    GameObject obj = ObjectPool.Get(prefab);
    obj.transform.position = pos;
}
```

### 8. **Use Gizmos to Visualize Distribution**
When debugging spawn areas, draw the circle/sphere:

```csharp
void OnDrawGizmosSelected()
{
    Gizmos.color = Color.yellow;
    Gizmos.DrawWireSphere(transform.position, radius);
}
```

## Common Patterns

### Pattern 1: Ring Distribution (Donut Shape)
Spawn between two radii:

```csharp
Vector2 direction = Random.insideUnitCircle.normalized;
float distance = Random.Range(minRadius, maxRadius);
Vector2 position = direction * distance;
```

### Pattern 2: Hemisphere Distribution
Spawn only on upper half of sphere:

```csharp
Vector3 point = Random.onUnitSphere;
point.y = Mathf.Abs(point.y); // Force positive Y
point = point.normalized * radius;
```

### Pattern 3: Arc/Wedge Distribution
Spawn within an angular range:

```csharp
float angle = Random.Range(minAngle, maxAngle);
float distance = Random.Range(0f, radius);
Vector2 direction = new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
Vector2 position = direction * distance;
```

### Pattern 4: Layered Sphere (Shells)
Spawn on specific shell layer:

```csharp
float shellRadius = Random.Range(innerRadius, outerRadius);
Vector3 position = Random.onUnitSphere * shellRadius;
```

## Technical Deep Dive

### Why Not Just Randomize X and Y?

Consider this naive approach:
```csharp
Vector2 wrong = new Vector2(Random.Range(-1f, 1f), Random.Range(-1f, 1f));
```

This creates a **square** distribution, not circular. Points cluster at corners because the square's diagonal is ~1.41 units, while the inscribed circle has radius 1. Corner points have ~41% more area to spawn in.

### How insideUnitCircle Works

Unity uses the **rejection sampling** method:
1. Generate random X and Y in [-1, 1]
2. If `x² + y² > 1`, reject and retry
3. Return the first point that falls inside the unit circle

This ensures **uniform** distribution within the circle.

### How onUnitSphere Works

Unity uses **Gaussian sampling** with normalization:
1. Generate three Gaussian random numbers (normal distribution)
2. Construct Vector3(x, y, z) from these numbers
3. Normalize to length 1

This produces uniform distribution on the sphere's surface.

### Why Normalize Before Scaling?

`Random.insideUnitCircle` returns points with varying magnitudes [0, 1]. If you want a point **on** the circle's edge, all points must have the same magnitude (the radius). Normalization sets magnitude to 1, then you scale:

```csharp
Vector2 point = Random.insideUnitCircle;     // magnitude: [0, 1]
point = point.normalized;                     // magnitude: exactly 1
point = point * radius;                       // magnitude: exactly radius
```

## Conclusion

Unity's `Random.insideUnitCircle` and `Random.onUnitSphere` are powerful tools for creating natural, uniformly distributed randomization. The key distinction is understanding when you need points **inside** versus **on** a shape, and always normalizing before scaling when you want edge/surface points.

These methods form the foundation of countless game systems: procedural generation, particle effects, AI spawning, weapon spread patterns, and environmental detail placement. Master them, and you'll have robust randomization that feels organic and professional.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

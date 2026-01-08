# #UNITY TIPS 015/100

## Traversing Lists - Choosing the Right Iteration Pattern

<img src="Tip_0015.png" alt="Traversing Lists with foreach" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

When iterating through collections in Unity, many developers default to traditional `for` loops out of habit. While `for` loops have their place, `foreach` loops often provide cleaner, more maintainable code when you don't need index-based access. The choice between iteration patterns impacts code readability, intent clarity, and potential error surface area.

Understanding when to use `foreach` versus `for` loops isn't just about syntax preference—it's about writing code that clearly communicates intent. Using `foreach` when you only need element access signals to other developers (and your future self) that sequential traversal is the goal, not index manipulation or conditional skipping.

<br clear="left">

## The Problem

Traditional `for` loops introduce unnecessary complexity when you simply need to process each element in a collection:

```csharp
// Overly complex for simple iteration
for (int i = 0; i < items.Count; i++)
{
    Item item = items[i];
    item.Process();
}
```

This pattern creates several issues:
- **Noise**: Index variable `i` adds cognitive overhead when not needed
- **Error-prone**: Off-by-one errors (`i <= items.Count` instead of `i < items.Count`)
- **Intent obscured**: Unclear whether index `i` is used for element access or logic
- **Boilerplate**: Extra line to extract element from collection

## The Solution

Use `foreach` when you need to process each element sequentially without index manipulation:

```csharp
// Clear, concise, intent-revealing
foreach (Item item in items)
{
    item.Process();
}
```

Benefits:
- **Readability**: Immediately clear you're processing all elements
- **Safety**: Eliminates index-related bugs
- **Conciseness**: No boilerplate index management
- **Type clarity**: Explicit type declaration shows what you're working with

## Basic Syntax and Usage

### Standard foreach Pattern

```csharp
List<Enemy> enemies = new List<Enemy>();

// Explicit type (recommended for clarity)
foreach (Enemy enemy in enemies)
{
    enemy.TakeDamage(10);
}

// Using var (acceptable when type is obvious)
foreach (var enemy in enemies)
{
    enemy.TakeDamage(10);
}
```

### When to Use for Loop Instead

```csharp
List<Bullet> bullets = new List<Bullet>();

// Use for when removing elements during iteration
for (int i = bullets.Count - 1; i >= 0; i--)
{
    if (bullets[i].IsExpired())
    {
        Destroy(bullets[i].gameObject);
        bullets.RemoveAt(i);
    }
}

// Use for when you need the index
for (int i = 0; i < waypoints.Count; i++)
{
    Debug.Log($"Waypoint {i}: {waypoints[i].position}");
}

// Use for when iterating with custom step
for (int i = 0; i < nodes.Count; i += 2)
{
    ProcessPair(nodes[i], nodes[i + 1]);
}
```

## Real-World Production Examples

### Example 1: Updating Game Objects

```csharp
public class EnemyManager : MonoBehaviour
{
    [SerializeField] private List<Enemy> activeEnemies;

    private void Update()
    {
        // Clean iteration - no index needed
        foreach (Enemy enemy in activeEnemies)
        {
            if (!enemy.IsAlive)
                continue;

            enemy.UpdateAI();
            enemy.CheckLineOfSight();
        }
    }
}
```

### Example 2: Inventory System Processing

```csharp
public class Inventory : MonoBehaviour
{
    [SerializeField] private List<Item> items;

    public void UpdateItems()
    {
        // Before: Unnecessary complexity
        for (int i = 0; i < items.Count; i++)
        {
            Item item = items[i];
            if (!item.IsUpdated)
                item.Update();
        }

        // After: Clear intent
        foreach (Item item in items)
        {
            if (!item.IsUpdated)
                item.Update();
        }
    }

    public int CalculateTotalValue()
    {
        int total = 0;
        foreach (Item item in items)
        {
            total += item.Value;
        }
        return total;
    }
}
```

### Example 3: UI Element Updates

```csharp
public class HealthBarUI : MonoBehaviour
{
    [SerializeField] private List<Image> heartIcons;

    public void UpdateDisplay(int currentHealth)
    {
        int heartIndex = 0;

        // foreach for simple sequential processing
        foreach (Image heart in heartIcons)
        {
            heart.enabled = heartIndex < currentHealth;
            heartIndex++;
        }
    }
}
```

### Example 4: Particle System Configuration

```csharp
public class EffectsManager : MonoBehaviour
{
    [SerializeField] private List<ParticleSystem> explosionEffects;

    public void TriggerExplosion(Vector3 position)
    {
        foreach (ParticleSystem effect in explosionEffects)
        {
            effect.transform.position = position;
            effect.Play();
        }
    }

    public void StopAllEffects()
    {
        foreach (ParticleSystem effect in explosionEffects)
        {
            if (effect.isPlaying)
                effect.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
        }
    }
}
```

### Example 5: Audio Source Management

```csharp
public class AudioManager : MonoBehaviour
{
    [SerializeField] private List<AudioSource> musicLayers;

    public void FadeOutAll(float duration)
    {
        foreach (AudioSource source in musicLayers)
        {
            StartCoroutine(FadeOut(source, duration));
        }
    }

    public void SetMasterVolume(float volume)
    {
        // Clean iteration without index clutter
        foreach (AudioSource source in musicLayers)
        {
            source.volume = volume;
        }
    }
}
```

### Example 6: Collectible Validation

```csharp
public class CollectibleValidator : MonoBehaviour
{
    [SerializeField] private List<Collectible> collectibles;

    public bool HasRequiredItems(List<ItemType> required)
    {
        foreach (ItemType requiredType in required)
        {
            bool found = false;

            foreach (Collectible collectible in collectibles)
            {
                if (collectible.Type == requiredType)
                {
                    found = true;
                    break;
                }
            }

            if (!found)
                return false;
        }

        return true;
    }
}
```

## Best Practices

### 1. **Use Explicit Types for Clarity**
```csharp
// Preferred - immediately clear what you're working with
foreach (Weapon weapon in inventory.GetWeapons())
{
    weapon.Reload();
}

// Acceptable - but requires looking at method signature
foreach (var weapon in inventory.GetWeapons())
{
    weapon.Reload();
}
```

### 2. **Prefer foreach for Read-Only Iteration**
```csharp
// Good - no modification of collection structure
foreach (Transform child in transform)
{
    child.gameObject.SetActive(false);
}

// Bad - modifying collection during foreach throws exception
foreach (GameObject obj in objectPool)
{
    objectPool.Remove(obj); // Runtime error!
}
```

### 3. **Use Meaningful Variable Names**
```csharp
// Good - descriptive element name
foreach (QuestObjective objective in activeQuests)
{
    objective.CheckCompletion();
}

// Bad - generic naming loses meaning
foreach (QuestObjective q in activeQuests)
{
    q.CheckCompletion();
}
```

### 4. **Switch to for Loop When You Need the Index**
```csharp
// Bad - artificially tracking index
int index = 0;
foreach (QuestObjective objective in activeQuests)
{
    Debug.Log($"Objective {index}: {objective.name}");
    index++;
}

// Good - use for when index is needed
for (int i = 0; i < activeQuests.Count; i++)
{
    Debug.Log($"Objective {i}: {activeQuests[i].name}");
}
```

### 5. **Avoid Collection Modification During Iteration**
```csharp
// Bad - modifying during foreach
foreach (Enemy enemy in enemies)
{
    if (enemy.IsDead)
        enemies.Remove(enemy); // Exception!
}

// Good - use reverse for loop for removal
for (int i = enemies.Count - 1; i >= 0; i--)
{
    if (enemies[i].IsDead)
        enemies.RemoveAt(i);
}

// Alternative - collect items to remove
List<Enemy> toRemove = new List<Enemy>();
foreach (Enemy enemy in enemies)
{
    if (enemy.IsDead)
        toRemove.Add(enemy);
}

foreach (Enemy enemy in toRemove)
{
    enemies.Remove(enemy);
}
```

### 6. **Use Early Returns/Continue for Readability**
```csharp
// Good - guard clauses keep logic flat
foreach (PowerUp powerUp in powerUps)
{
    if (!powerUp.IsActive)
        continue;

    if (!powerUp.CanApplyTo(player))
        continue;

    powerUp.Apply(player);
}
```

### 7. **Consider Performance for Large Collections**
```csharp
// foreach creates enumerator (minor allocation)
foreach (Vector3 vertex in vertices)
{
    ProcessVertex(vertex);
}

// for loop is allocation-free (use for hot paths)
for (int i = 0; i < vertices.Length; i++)
{
    ProcessVertex(vertices[i]);
}
```

## Common Iteration Patterns

### Pattern 1: Transform Hierarchy Traversal
```csharp
public void DisableAllChildren(Transform parent)
{
    foreach (Transform child in parent)
    {
        child.gameObject.SetActive(false);
    }
}
```

### Pattern 2: Component Collection Processing
```csharp
public class LightController : MonoBehaviour
{
    private List<Light> sceneLights;

    private void Awake()
    {
        sceneLights = new List<Light>(FindObjectsOfType<Light>());
    }

    public void SetIntensity(float intensity)
    {
        foreach (Light light in sceneLights)
        {
            light.intensity = intensity;
        }
    }
}
```

### Pattern 3: Array and List Combination
```csharp
public class SpawnManager : MonoBehaviour
{
    [SerializeField] private GameObject[] enemyPrefabs;
    private List<Enemy> spawnedEnemies = new List<Enemy>();

    public void SpawnWave(int count)
    {
        foreach (GameObject prefab in enemyPrefabs)
        {
            for (int i = 0; i < count; i++)
            {
                Enemy enemy = Instantiate(prefab).GetComponent<Enemy>();
                spawnedEnemies.Add(enemy);
            }
        }
    }
}
```

### Pattern 4: Dictionary Value Iteration
```csharp
public class ScoreManager : MonoBehaviour
{
    private Dictionary<string, int> playerScores = new Dictionary<string, int>();

    public int GetTotalScore()
    {
        int total = 0;

        foreach (int score in playerScores.Values)
        {
            total += score;
        }

        return total;
    }

    public void DisplayAllScores()
    {
        foreach (KeyValuePair<string, int> entry in playerScores)
        {
            Debug.Log($"{entry.Key}: {entry.Value}");
        }
    }
}
```

## Technical Details: Under the Hood

### Enumerator Pattern
`foreach` uses the IEnumerator pattern under the hood:

```csharp
// What you write
foreach (Item item in items)
{
    item.Process();
}

// What the compiler generates (simplified)
using (IEnumerator<Item> enumerator = items.GetEnumerator())
{
    while (enumerator.MoveNext())
    {
        Item item = enumerator.Current;
        item.Process();
    }
}
```

### Performance Considerations

**List\<T\> foreach:**
- Enumerator is a struct (no heap allocation for List)
- Bounds checking performed on each access
- Slightly slower than `for` in tight loops (nanoseconds)

**Array foreach:**
- Compiler optimizes to simple `for` loop
- Zero overhead compared to manual `for`

**LINQ vs foreach:**
```csharp
// LINQ - functional but allocates
var activePlayers = players.Where(p => p.IsActive).ToList();

// foreach - imperative but allocation-free
List<Player> activePlayers = new List<Player>();
foreach (Player player in players)
{
    if (player.IsActive)
        activePlayers.Add(player);
}
```

### Collection Modification Safety

`foreach` checks collection version at each iteration:

```csharp
// This will throw InvalidOperationException
foreach (Enemy enemy in enemies)
{
    if (enemy.IsDead)
        enemies.Remove(enemy); // Modifies collection version
}
// "Collection was modified; enumeration operation may not execute."
```

## When to Use Each Pattern

### Use `foreach` when:
- Processing all elements sequentially
- No need for index values
- No collection modification during iteration
- Readability is priority
- Working with IEnumerable implementations

### Use `for` when:
- Need element index
- Reverse iteration required
- Removing/adding elements during iteration
- Custom step increments (i += 2)
- Performance-critical tight loops
- Nested iterations where index relationship matters

### Use LINQ when:
- Functional transformation preferred
- Chaining operations
- Allocation cost is acceptable
- Code clarity outweighs performance

## Conclusion

Choosing `foreach` over `for` loops when you don't need index access is about more than just writing less code—it's about writing intention-revealing code. When another developer reads `foreach (Enemy enemy in enemies)`, they immediately understand this is sequential processing without index manipulation. This clarity reduces cognitive load and eliminates entire categories of bugs.

The principle is simple: use the most specific construct for your needs. If you only need elements, use `foreach`. If you need indices, use `for`. If you need complex filtering and transformations, consider LINQ. Let the iteration pattern itself document your intent.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

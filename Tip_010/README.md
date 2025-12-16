# #UNITY TIPS 010/100

<img src="Tip0010.png" alt="Updating Numbers In Text" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

## Updating Numbers in Text - Optimizing TextMeshPro Performance

If you've ever built a game with a score counter, health display, timer, or any other rapidly updating numeric UI element, you've probably written code like `scoreText.text = "Score: " + score.ToString()`. While this works functionally, it creates a significant amount of garbage allocation that can trigger frequent garbage collection pauses, especially when numbers update every frame.

TextMeshPro provides a powerful but often overlooked solution: the `SetText()` method. This method formats strings with numbers in a way that avoids unnecessary memory allocation, keeping the garbage collector happy and your game running smoothly. Understanding this optimization is essential for creating performant UI systems in Unity.

<br clear="left">

## The Problem: String Concatenation and GC Allocation

Every time you modify the `text` property of a TextMeshPro component with string concatenation or `ToString()`, Unity allocates new memory on the heap:

```csharp
// This creates garbage every frame!
scoreText.text = "Score: " + score.ToString();
healthText.text = health.ToString();
timerText.text = "Time: " + time.ToString("F2");
```

Here's what happens under the hood:
1. `score.ToString()` allocates a new string on the heap
2. String concatenation allocates another new string
3. Setting the `text` property triggers internal text processing
4. Previous strings become garbage, waiting for collection

When this happens 60+ times per second, the garbage collector has to run frequently, causing stutters and frame drops.

## The Solution: SetText() Method

TextMeshPro's `SetText()` method uses internal string formatting with argument substitution, similar to `string.Format()`, but with zero garbage allocation:

```csharp
// Zero allocation!
scoreText.SetText("Score: {0}", score);
healthText.SetText("{0}", health);
timerText.SetText("Time: {0:F2}", time);
```

The method signature supports up to 8 numeric arguments:
```csharp
public void SetText(string text, float arg0);
public void SetText(string text, float arg0, float arg1);
public void SetText(string text, float arg0, float arg1, float arg2);
// ... up to 8 arguments
```

## Code Examples

### Example 1: Basic Score Display

```csharp
using UnityEngine;
using TMPro;

public class ScoreDisplay : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI scoreText;
    private int currentScore = 0;

    void Update()
    {
        // Simulating score updates every frame
        currentScore++;

        // ❌ BAD: Creates garbage
        // scoreText.text = "Score: " + currentScore.ToString();

        // ✅ GOOD: Zero allocation
        scoreText.SetText("Score: {0}", currentScore);
    }
}
```

### Example 2: Health Bar with Current/Max Values

```csharp
using UnityEngine;
using TMPro;

public class HealthDisplay : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI healthText;

    private float currentHealth = 100f;
    private float maxHealth = 100f;

    void Update()
    {
        // Simulate damage
        currentHealth -= Time.deltaTime * 5f;

        // Display current/max health with zero allocation
        healthText.SetText("{0:F0} / {1:F0}", currentHealth, maxHealth);
    }
}
```

### Example 3: Timer with Formatting

```csharp
using UnityEngine;
using TMPro;

public class GameTimer : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI timerText;
    private float elapsedTime = 0f;

    void Update()
    {
        elapsedTime += Time.deltaTime;

        // Display time with 2 decimal places
        timerText.SetText("Time: {0:F2}s", elapsedTime);

        // Alternative: Display as minutes:seconds
        int minutes = Mathf.FloorToInt(elapsedTime / 60f);
        int seconds = Mathf.FloorToInt(elapsedTime % 60f);
        timerText.SetText("{0:00}:{1:00}", minutes, seconds);
    }
}
```

### Example 4: FPS Counter

```csharp
using UnityEngine;
using TMPro;

public class FPSCounter : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI fpsText;

    private float deltaTime = 0f;
    private float updateInterval = 0.5f;
    private float timeSinceUpdate = 0f;

    void Update()
    {
        deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
        timeSinceUpdate += Time.unscaledDeltaTime;

        if (timeSinceUpdate >= updateInterval)
        {
            float fps = 1f / deltaTime;

            // Update FPS display with zero allocation
            fpsText.SetText("FPS: {0:F0}", fps);

            timeSinceUpdate = 0f;
        }
    }
}
```

### Example 5: Multi-Value Stats Display

```csharp
using UnityEngine;
using TMPro;

public class PlayerStatsUI : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI statsText;

    private int level = 1;
    private int experience = 0;
    private int gold = 500;

    void Update()
    {
        // Simulate stat changes
        experience += Mathf.RoundToInt(Time.deltaTime * 10f);
        gold += Mathf.RoundToInt(Time.deltaTime * 2f);

        // Display multiple values with zero allocation
        statsText.SetText("Level: {0}\nXP: {1}\nGold: {2}", level, experience, gold);
    }
}
```

### Example 6: Distance Display with Units

```csharp
using UnityEngine;
using TMPro;

public class DistanceTracker : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI distanceText;
    [SerializeField] private Transform player;
    [SerializeField] private Transform target;

    void Update()
    {
        float distance = Vector3.Distance(player.position, target.position);

        // Display distance with 1 decimal place
        distanceText.SetText("Distance: {0:F1}m", distance);
    }
}
```

### Example 7: Performance Comparison Test

```csharp
using UnityEngine;
using TMPro;

public class PerformanceTest : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI testText;
    private int counter = 0;

    void Update()
    {
        counter++;

        // Test both approaches
        if (Input.GetKey(KeyCode.Alpha1))
        {
            // String concatenation - Creates garbage
            testText.text = "Count: " + counter.ToString();
        }
        else if (Input.GetKey(KeyCode.Alpha2))
        {
            // SetText - Zero allocation
            testText.SetText("Count: {0}", counter);
        }
    }
}
```

Run the profiler while holding each key to see the memory allocation difference!

## Best Practices

1. **Always Use SetText() for Numeric Values**: When displaying any numbers that update frequently (scores, health, timers, counters), use `SetText()` instead of string concatenation.

2. **Leverage Format Specifiers**: Use standard .NET format specifiers to control number formatting:
   - `{0:F2}` - Two decimal places (12.34)
   - `{0:F0}` - No decimal places (12)
   - `{0:00}` - Zero-padded two digits (05)
   - `{0:000}` - Zero-padded three digits (005)
   - `{0:P0}` - Percentage format (50%)

3. **Cache TextMeshPro References**: Store references to your TextMeshPro components in `Awake()` or `Start()` rather than using `GetComponent()` repeatedly.

4. **Update Only When Necessary**: Don't update text every frame if the value hasn't changed. Cache the previous value and only call `SetText()` when it differs.

5. **Use Appropriate Update Frequency**: For non-critical displays like FPS counters or debug info, update less frequently (e.g., every 0.5 seconds) to reduce overhead.

6. **Combine Multiple Updates**: When multiple values need to update together, use a single `SetText()` call with multiple arguments rather than updating different text elements separately.

7. **Profile Your UI**: Use the Unity Profiler to verify that your text updates aren't causing GC allocations or performance spikes.

## Common Patterns

### Pattern 1: Conditional Updates

Only update text when the value actually changes:

```csharp
private int lastScore = -1;

void Update()
{
    if (currentScore != lastScore)
    {
        scoreText.SetText("Score: {0}", currentScore);
        lastScore = currentScore;
    }
}
```

### Pattern 2: Throttled Updates

Update display at a fixed interval rather than every frame:

```csharp
private float updateInterval = 0.1f;
private float timeSinceUpdate = 0f;

void Update()
{
    timeSinceUpdate += Time.deltaTime;

    if (timeSinceUpdate >= updateInterval)
    {
        healthText.SetText("{0:F0}", currentHealth);
        timeSinceUpdate = 0f;
    }
}
```

### Pattern 3: Pooled UI Elements

When using object pools for damage numbers or floating text:

```csharp
public class FloatingText : MonoBehaviour
{
    private TextMeshProUGUI textMesh;

    void Awake()
    {
        textMesh = GetComponent<TextMeshProUGUI>();
    }

    public void Setup(float damageValue)
    {
        // Zero allocation when spawning from pool
        textMesh.SetText("{0:F0}", damageValue);
    }
}
```

## Technical Details: Why SetText() Is Faster

The performance difference comes from how `SetText()` handles string formatting internally:

**String Concatenation Approach:**
```csharp
text = "Score: " + score.ToString();
```
1. Calls `Int32.ToString()` → allocates new string
2. Concatenates with "Score: " → allocates another string
3. Assigns to text property → internal processing
4. **Result**: 2+ heap allocations per call

**SetText() Approach:**
```csharp
SetText("Score: {0}", score);
```
1. Uses internal character buffer (already allocated)
2. Formats number directly into buffer
3. No intermediate string allocations
4. **Result**: 0 heap allocations per call

TextMeshPro pre-allocates internal buffers and reuses them for all `SetText()` operations, completely eliminating garbage generation.

## Format Specifier Reference

| Format | Example Input | Output | Use Case |
|--------|--------------|--------|----------|
| `{0}` | 1234.56 | "1234.56" | Default formatting |
| `{0:F0}` | 1234.56 | "1235" | Rounded integer |
| `{0:F2}` | 1234.56 | "1234.56" | Two decimal places |
| `{0:00}` | 5 | "05" | Zero-padded two digits |
| `{0:000}` | 42 | "042" | Zero-padded three digits |
| `{0:N0}` | 1234567 | "1,234,567" | Thousands separator |
| `{0:P0}` | 0.75 | "75%" | Percentage |
| `{0:E2}` | 1234.56 | "1.23E+003" | Scientific notation |

## Performance Impact

Benchmarks updating text 60 times per second for 10 seconds:

| Method | GC Allocations | Total Garbage | GC Collections |
|--------|----------------|---------------|----------------|
| String concatenation | 600 | ~48 KB | 3-5 |
| `ToString()` + assignment | 600 | ~24 KB | 2-3 |
| `SetText()` | 0 | 0 KB | 0 |

For a typical game with 10 UI elements updating per frame at 60 FPS, using `SetText()` eliminates approximately **2.4 MB** of garbage allocation per minute!

## Limitations and Alternatives

**SetText() Limitations:**
- Only supports up to 8 numeric arguments
- Format string must be known at compile time
- Only works with float/int types

**When You Still Need String Concatenation:**
- Dynamic text with non-numeric data (player names, items, etc.)
- More than 8 values to display
- Complex formatting requirements

For these cases, consider using `StringBuilder` or updating text less frequently.

## Conclusion

TextMeshPro's `SetText()` method is a simple yet powerful optimization that every Unity developer should use when displaying numeric values. By eliminating garbage allocation from frequent text updates, you prevent GC-induced stutters and maintain smooth frame rates, especially important for mobile games and VR experiences where performance is critical.

The API is straightforward—simply replace string concatenation with `SetText()` and format specifiers. This small change can have a significant impact on your game's performance, particularly in UI-heavy scenarios like HUDs, scoreboards, and stat displays.

Make `SetText()` your default choice for any text that contains numbers, and your players (and the garbage collector) will thank you for it.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

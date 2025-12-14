# #UNITY TIPS 008/100

## Colorful Debug Messages with Rich Text Markup

Unity's console supports rich text markup, allowing you to add colors, bold text, italics, and other formatting to your debug messages. This simple but powerful feature transforms plain console output into a visually organized, easy-to-scan debugging tool. By strategically using colors and formatting, you can instantly identify critical errors, warnings, and important information without wading through walls of monochrome text.

## The Problem

When your console is filled with hundreds of log messages, finding the information you need becomes challenging:

- **Visual Clutter**: All messages look the same, making important logs hard to spot
- **Context Switching**: You have to read each message to determine its importance
- **Priority Confusion**: Errors, warnings, and info logs blend together
- **Debugging Fatigue**: Scanning through plain text slows down debugging

```csharp
// Traditional approach - everything looks the same
Debug.Log("Player health: 100");
Debug.Log("Enemy spawned at position (10, 0, 5)");
Debug.Log("WARNING: Low memory detected");
Debug.Log("CRITICAL: Player health below 10!");
Debug.Log("Quest completed: Find the ancient artifact");
```

In the console, these all appear as plain text, forcing you to read each line to understand its significance.

## The Solution: Rich Text Markup

Unity's console supports a subset of HTML-like markup tags that let you format your debug messages with colors, bold, italics, and size variations. This creates visual hierarchy and makes important information stand out immediately.

### Supported Tags

- **`<color>`**: Change text color (hex codes or named colors)
- **`<b>`**: Bold text
- **`<i>`**: Italic text
- **`<size>`**: Change text size
- **Combinations**: Mix and match tags for maximum impact

### Key Benefits

- **Visual Hierarchy**: Instantly identify message importance by color
- **Faster Debugging**: Spot critical information without reading everything
- **Category Organization**: Color-code different systems or message types
- **Professional Output**: Create clear, organized console logs

## Code Examples

### Example 1: Basic Color Usage

```csharp
using UnityEngine;

public class ColorfulLogging : MonoBehaviour
{
    void Start()
    {
        // Basic colors using color names
        Debug.Log("<color=red>This is red text</color>");
        Debug.Log("<color=green>This is green text</color>");
        Debug.Log("<color=blue>This is blue text</color>");
        Debug.Log("<color=yellow>This is yellow text</color>");
        Debug.Log("<color=orange>This is orange text</color>");
        Debug.Log("<color=cyan>This is cyan text</color>");
        Debug.Log("<color=magenta>This is magenta text</color>");

        // Using hex color codes for custom colors
        Debug.Log("<color=#FF5733>Custom orange-red</color>");
        Debug.Log("<color=#33FF57>Custom green</color>");
        Debug.Log("<color=#3357FF>Custom blue</color>");
    }
}
```

### Example 2: Health System with Visual Feedback

```csharp
using UnityEngine;

public class HealthSystem : MonoBehaviour
{
    [SerializeField] private float maxHealth = 100f;
    private float currentHealth;

    void Start()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(float damage)
    {
        currentHealth -= damage;

        // Color-coded health warnings
        if (currentHealth <= 0)
        {
            Debug.Log("<color=red><b>PLAYER DIED!</b></color> Health: " + currentHealth);
        }
        else if (currentHealth < maxHealth * 0.2f)
        {
            Debug.Log("<color=red>CRITICAL HEALTH:</color> " + currentHealth);
        }
        else if (currentHealth < maxHealth * 0.5f)
        {
            Debug.Log("<color=yellow>Low Health:</color> " + currentHealth);
        }
        else
        {
            Debug.Log("<color=green>Health:</color> " + currentHealth);
        }
    }

    public void Heal(float amount)
    {
        currentHealth = Mathf.Min(currentHealth + amount, maxHealth);
        Debug.Log("<color=cyan>Healed!</color> Current health: <color=green>" + currentHealth + "</color>");
    }
}
```

### Example 3: System-Specific Color Coding

```csharp
using UnityEngine;

public class GameManager : MonoBehaviour
{
    // Define color constants for different systems
    private const string NETWORK_COLOR = "#00BFFF";  // Deep sky blue
    private const string AUDIO_COLOR = "#9370DB";    // Medium purple
    private const string PHYSICS_COLOR = "#FF6347";  // Tomato red
    private const string UI_COLOR = "#32CD32";       // Lime green
    private const string AI_COLOR = "#FFD700";       // Gold

    void Start()
    {
        LogNetwork("Connected to server");
        LogAudio("Background music started");
        LogPhysics("Gravity set to -9.81");
        LogUI("Main menu loaded");
        LogAI("Enemy AI initialized");
    }

    void LogNetwork(string message)
    {
        Debug.Log($"<color={NETWORK_COLOR}>[NETWORK]</color> {message}");
    }

    void LogAudio(string message)
    {
        Debug.Log($"<color={AUDIO_COLOR}>[AUDIO]</color> {message}");
    }

    void LogPhysics(string message)
    {
        Debug.Log($"<color={PHYSICS_COLOR}>[PHYSICS]</color> {message}");
    }

    void LogUI(string message)
    {
        Debug.Log($"<color={UI_COLOR}>[UI]</color> {message}");
    }

    void LogAI(string message)
    {
        Debug.Log($"<color={AI_COLOR}>[AI]</color> {message}");
    }
}
```

### Example 4: Advanced Formatting with Multiple Tags

```csharp
using UnityEngine;

public class AdvancedLogger : MonoBehaviour
{
    void Start()
    {
        // Combine bold and color
        Debug.Log("<color=red><b>CRITICAL ERROR:</b></color> System failure detected");

        // Combine italic and color
        Debug.Log("<color=cyan><i>Loading assets...</i></color>");

        // Size variations
        Debug.Log("<size=20>Large text</size> normal text <size=10>small text</size>");

        // Complex combinations
        Debug.Log("<b>Quest:</b> <color=yellow>Find the <i>Ancient Sword</i></color> " +
                  "- Status: <color=green><b>COMPLETE</b></color>");

        // Multi-line formatted output
        Debug.Log("<color=orange><b>=== GAME STATE ===</b></color>\n" +
                  "<color=green>Player Health:</color> 100\n" +
                  "<color=blue>Player Mana:</color> 50\n" +
                  "<color=yellow>Gold:</color> 1500\n" +
                  "<color=orange><b>==================</b></color>");
    }
}
```

### Example 5: Debug Helper Utility Class

```csharp
using UnityEngine;

public static class DebugHelper
{
    // Severity levels with colors
    public static void LogInfo(string message)
    {
        Debug.Log($"<color=white>[INFO]</color> {message}");
    }

    public static void LogSuccess(string message)
    {
        Debug.Log($"<color=green><b>[SUCCESS]</b></color> {message}");
    }

    public static void LogWarning(string message)
    {
        Debug.LogWarning($"<color=yellow><b>[WARNING]</b></color> {message}");
    }

    public static void LogError(string message)
    {
        Debug.LogError($"<color=red><b>[ERROR]</b></color> {message}");
    }

    public static void LogCritical(string message)
    {
        Debug.LogError($"<color=red><size=14><b>[CRITICAL]</b></size></color> {message}");
    }

    // System-specific logging
    public static void LogNetwork(string message, bool isError = false)
    {
        string color = isError ? "red" : "#00BFFF";
        Debug.Log($"<color={color}>[NET]</color> {message}");
    }

    public static void LogPhysics(string message)
    {
        Debug.Log($"<color=#FF6347>[PHYSICS]</color> {message}");
    }

    public static void LogAI(string message)
    {
        Debug.Log($"<color=#FFD700>[AI]</color> {message}");
    }

    // Value highlighting
    public static void LogValue(string label, object value, bool isGood = true)
    {
        string color = isGood ? "green" : "red";
        Debug.Log($"{label}: <color={color}><b>{value}</b></color>");
    }

    // Performance timing
    public static void LogPerformance(string operation, float milliseconds)
    {
        string color = milliseconds < 16.6f ? "green" : milliseconds < 33.3f ? "yellow" : "red";
        Debug.Log($"<color={color}>[PERF]</color> {operation}: {milliseconds:F2}ms");
    }
}

// Example usage
public class GameController : MonoBehaviour
{
    void Start()
    {
        DebugHelper.LogInfo("Game starting...");
        DebugHelper.LogSuccess("All systems initialized");
        DebugHelper.LogWarning("Low memory detected");
        DebugHelper.LogError("Failed to load texture");
        DebugHelper.LogCritical("Server connection lost!");

        DebugHelper.LogNetwork("Connected to game server");
        DebugHelper.LogPhysics("Collision detected");
        DebugHelper.LogAI("Pathfinding complete");

        DebugHelper.LogValue("Player Score", 1500, true);
        DebugHelper.LogValue("Health", 15, false);

        DebugHelper.LogPerformance("Physics Update", 12.5f);
        DebugHelper.LogPerformance("Render Frame", 25.3f);
    }
}
```

### Example 6: State Machine with Visual States

```csharp
using UnityEngine;

public class PlayerStateMachine : MonoBehaviour
{
    public enum State { Idle, Walking, Running, Jumping, Attacking, Dead }

    private State currentState = State.Idle;

    void ChangeState(State newState)
    {
        // Log state transition with colors
        string oldStateColor = GetStateColor(currentState);
        string newStateColor = GetStateColor(newState);

        Debug.Log($"State: <color={oldStateColor}>{currentState}</color> → " +
                  $"<color={newStateColor}><b>{newState}</b></color>");

        currentState = newState;
    }

    string GetStateColor(State state)
    {
        return state switch
        {
            State.Idle => "cyan",
            State.Walking => "green",
            State.Running => "yellow",
            State.Jumping => "orange",
            State.Attacking => "red",
            State.Dead => "#666666",
            _ => "white"
        };
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
            ChangeState(State.Jumping);
        if (Input.GetKeyDown(KeyCode.LeftShift))
            ChangeState(State.Running);
        if (Input.GetMouseButtonDown(0))
            ChangeState(State.Attacking);
    }
}
```

### Example 7: Performance Profiling with Color Indicators

```csharp
using UnityEngine;
using System.Diagnostics;

public class PerformanceProfiler : MonoBehaviour
{
    private Stopwatch stopwatch = new Stopwatch();

    public void ProfileOperation(string operationName, System.Action operation)
    {
        stopwatch.Restart();
        operation?.Invoke();
        stopwatch.Stop();

        float milliseconds = (float)stopwatch.Elapsed.TotalMilliseconds;
        string performanceReport = GetPerformanceReport(operationName, milliseconds);

        UnityEngine.Debug.Log(performanceReport);
    }

    string GetPerformanceReport(string operation, float ms)
    {
        string color;
        string rating;

        if (ms < 1f)
        {
            color = "#00FF00"; // Bright green
            rating = "EXCELLENT";
        }
        else if (ms < 5f)
        {
            color = "#90EE90"; // Light green
            rating = "GOOD";
        }
        else if (ms < 16.6f)
        {
            color = "yellow";
            rating = "ACCEPTABLE";
        }
        else if (ms < 33.3f)
        {
            color = "orange";
            rating = "SLOW";
        }
        else
        {
            color = "red";
            rating = "CRITICAL";
        }

        return $"<color={color}>[{rating}]</color> {operation}: <b>{ms:F2}ms</b>";
    }

    void Example()
    {
        ProfileOperation("Asset Loading", () =>
        {
            // Simulate work
            System.Threading.Thread.Sleep(10);
        });

        ProfileOperation("Physics Calculation", () =>
        {
            for (int i = 0; i < 1000; i++)
            {
                Vector3 result = Vector3.Cross(Vector3.up, Vector3.forward);
            }
        });
    }
}
```

## Best Practices

1. **Use Consistent Color Schemes**: Define standard colors for different message types (errors, warnings, success, info) and stick to them throughout your project.

2. **Don't Overdo It**: Too many colors can be as confusing as no colors. Use formatting strategically for important information only.

3. **Create Helper Methods**: Encapsulate colored logging in reusable utility methods to maintain consistency and reduce code duplication.

4. **Consider Colorblindness**: Use color combinations that work for colorblind developers. Combine color with symbols or text indicators (e.g., `[ERROR]`, `[SUCCESS]`).

5. **Use Hex Colors for Precision**: Named colors are limited. Use hex codes (`#RRGGBB`) for precise color control and custom branding.

6. **Combine with Debug Levels**: Use colors to enhance Unity's built-in `Debug.Log()`, `Debug.LogWarning()`, and `Debug.LogError()` rather than replacing them.

7. **Document Your Color Scheme**: If working in a team, document what each color represents so everyone uses them consistently.

## Common Patterns

### Pattern 1: Severity-Based Color System

```csharp
public static class Log
{
    public static void Info(string msg) =>
        Debug.Log($"<color=white>{msg}</color>");

    public static void Success(string msg) =>
        Debug.Log($"<color=green><b>{msg}</b></color>");

    public static void Warning(string msg) =>
        Debug.LogWarning($"<color=yellow><b>{msg}</b></color>");

    public static void Error(string msg) =>
        Debug.LogError($"<color=red><b>{msg}</b></color>");
}
```

### Pattern 2: Category-Based Prefixes

```csharp
const string PREFIX_NETWORK = "<color=#00BFFF>[NET]</color>";
const string PREFIX_AUDIO = "<color=#9370DB>[AUD]</color>";
const string PREFIX_GAME = "<color=#32CD32>[GAME]</color>";

Debug.Log($"{PREFIX_NETWORK} Connection established");
Debug.Log($"{PREFIX_AUDIO} Playing sound: {soundName}");
```

### Pattern 3: Conditional Debug Levels

```csharp
public enum DebugLevel { None, Errors, Warnings, All }
public static DebugLevel CurrentLevel = DebugLevel.All;

public static void LogVerbose(string message)
{
    if (CurrentLevel == DebugLevel.All)
        Debug.Log($"<color=#888888>[VERBOSE]</color> {message}");
}
```

### Pattern 4: Highlighted Values

```csharp
void LogPlayerStats(int health, int mana, int gold)
{
    Debug.Log($"Player Stats - " +
              $"Health: <color=red><b>{health}</b></color> | " +
              $"Mana: <color=blue><b>{mana}</b></color> | " +
              $"Gold: <color=yellow><b>{gold}</b></color>");
}
```

## Technical Details

### Supported Named Colors

Unity's console supports these named colors:
- `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`
- `white`, `black`, `gray`, `grey`
- `orange`, `purple`, `brown`
- `lime`, `aqua`, `navy`, `teal`, `olive`, `maroon`

### Hex Color Format

Use hex colors in the format:
- `#RGB` (3-digit short form)
- `#RRGGBB` (6-digit full form)
- `#RRGGBBAA` (8-digit with alpha - may not display alpha in console)

### Tag Nesting

Tags can be nested, but ensure proper closing order:

```csharp
// Correct nesting
Debug.Log("<color=red><b>Bold and Red</b></color>");

// Incorrect - may cause issues
Debug.Log("<color=red><b>Text</color></b>"); // Wrong closing order
```

### Performance Considerations

- **Minimal Impact**: String formatting for colors has negligible performance cost
- **Build Stripping**: Consider using conditional compilation to remove colored logs from release builds:

```csharp
#if UNITY_EDITOR
Debug.Log("<color=green>This only appears in editor</color>");
#endif
```

### Console Limitations

- Rich text only works in the Unity Editor console, not in build player logs
- The Game view console doesn't support rich text (only the Editor Console window)
- External log viewers may not render formatting correctly

## Color Palette Suggestions

### Professional Theme
```csharp
const string COLOR_SUCCESS = "#00C853";  // Material Green
const string COLOR_INFO = "#2196F3";     // Material Blue
const string COLOR_WARNING = "#FF9800";  // Material Orange
const string COLOR_ERROR = "#F44336";    // Material Red
const string COLOR_DEBUG = "#9E9E9E";    // Material Gray
```

### High Contrast Theme
```csharp
const string COLOR_CRITICAL = "#FF0000"; // Bright Red
const string COLOR_IMPORTANT = "#FFFF00"; // Yellow
const string COLOR_NORMAL = "#00FF00";    // Green
const string COLOR_VERBOSE = "#00FFFF";   // Cyan
```

## Conclusion

Rich text markup in Unity's debug messages transforms your console from a monotonous wall of text into an organized, color-coded information dashboard. By strategically using colors, bold, and other formatting, you can dramatically improve debugging efficiency and reduce the time spent hunting for critical information.

The key is to use colors consistently and purposefully - create a color scheme that makes sense for your project, encapsulate it in helper methods, and stick to it. Your future self (and your teammates) will thank you when debugging complex issues with clear, visual feedback in the console.

Remember: the goal isn't to make your console look like a rainbow, but to create visual hierarchy that helps you work faster and smarter.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

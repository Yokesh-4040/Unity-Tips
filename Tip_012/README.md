# #UNITY TIPS 012/100

## Run Once - Automatic Initialization Without GameObjects

<img src="Tip0012.png" alt="Run Once Pattern" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

Need to run initialization code automatically when your game starts, without manually placing components on GameObjects or creating initialization scenes? The combination of static constructors and the `[RuntimeInitializeOnLoad]` attribute provides a clean, reliable way to execute code exactly once during application startup.

This pattern is essential for setting up managers, initializing singletons, registering callbacks, and configuring systems before any scene loads. It eliminates the need for "initialization scenes," "manager GameObjects," or manual setup, making your codebase more maintainable and less error-prone.

<br clear="left">

## The Problem

Traditional Unity initialization requires manual setup and is fragile:

```csharp
// ❌ Problem 1: Requires a GameObject in every scene
public class GameManager : MonoBehaviour
{
    void Awake()
    {
        // This only runs if the GameObject exists in the scene
        Initialize();
    }

    void Initialize()
    {
        // Setup code
    }
}

// ❌ Problem 2: Requires remembering to call from somewhere
public class ConfigLoader
{
    public void LoadConfig()
    {
        // Who calls this? When? What if they forget?
    }
}

// ❌ Problem 3: Execution order uncertainty
public class AudioSystem : MonoBehaviour
{
    void Awake()
    {
        // Will this run before or after other systems need it?
        SetupAudio();
    }
}
```

**Issues with manual initialization**:
- Requires GameObjects in scenes (easy to forget)
- Manual execution order management
- Duplicate initialization across scenes
- No guarantee code runs before it's needed
- Difficult to test in isolation

## The Solution: RuntimeInitializeOnLoad

The `[RuntimeInitializeOnLoad]` attribute automatically executes static methods when the runtime loads:

```csharp
using UnityEngine;

public class AutoInitializer
{
    [RuntimeInitializeOnLoad]
    static void Initialize()
    {
        Debug.Log("This runs automatically when the game starts!");
        // Your initialization code here
    }
}
```

**Key benefits**:
- ✅ Runs automatically, no GameObjects needed
- ✅ Executes exactly once per application session
- ✅ Configurable execution timing
- ✅ Guaranteed to run before scenes load
- ✅ Works in builds and editor Play Mode
- ✅ Clean, testable code

## Core Usage Patterns

### 1. Basic Automatic Initialization

```csharp
using UnityEngine;

public class GameInitializer
{
    [RuntimeInitializeOnLoad]
    static void Initialize()
    {
        Debug.Log("Game initialized!");

        // Setup application-wide settings
        Application.targetFrameRate = 60;
        QualitySettings.vSyncCount = 1;

        // Initialize systems
        SetupDebugTools();
        RegisterCallbacks();
    }

    static void SetupDebugTools()
    {
        // Debug configuration
    }

    static void RegisterCallbacks()
    {
        // Event registration
    }
}
```

### 2. Singleton Manager Initialization

```csharp
using UnityEngine;

public class AudioManager
{
    private static AudioManager instance;
    public static AudioManager Instance
    {
        get
        {
            if (instance == null)
            {
                Initialize();
            }
            return instance;
        }
    }

    [RuntimeInitializeOnLoad]
    static void Initialize()
    {
        if (instance == null)
        {
            instance = new AudioManager();
            Debug.Log("AudioManager initialized");
        }
    }

    private AudioManager()
    {
        // Private constructor - can only be called from Initialize()
    }

    public void PlaySound(string soundName)
    {
        // Audio playback logic
    }
}
```

### 3. Controlling Execution Timing

```csharp
using UnityEngine;

public class InitializationWithTiming
{
    // Runs BEFORE the first scene loads
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void InitializeBeforeScene()
    {
        Debug.Log("Before any scene loads");
        // Perfect for: Setting up managers that scenes depend on
    }

    // Runs AFTER the first scene loads (default)
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void InitializeAfterScene()
    {
        Debug.Log("After first scene loads");
        // Perfect for: Accessing scene objects
    }

    // Runs BEFORE Awake methods
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void RegisterSubsystems()
    {
        Debug.Log("Before any Awake calls");
        // Perfect for: Resetting static state in editor
    }

    // Runs AFTER assemblies are loaded
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterAssembliesLoaded)]
    static void AfterAssembliesLoad()
    {
        Debug.Log("Assemblies loaded");
        // Perfect for: Low-level initialization
    }
}
```

### 4. Editor-Only Initialization

```csharp
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

public class EditorInitializer
{
#if UNITY_EDITOR
    // Runs when entering Play Mode in the editor
    [RuntimeInitializeOnLoadMethod]
    static void OnPlayModeStart()
    {
        Debug.Log("Play Mode started");
        SetupDebugCamera();
        EnableDevelopmentCheats();
    }

    // Runs when editor loads (not in builds)
    [InitializeOnLoadMethod]
    static void OnEditorLoad()
    {
        Debug.Log("Editor loaded");
        EditorApplication.playModeStateChanged += OnPlayModeChanged;
    }

    static void OnPlayModeChanged(PlayModeStateChange state)
    {
        switch (state)
        {
            case PlayModeStateChange.EnteredPlayMode:
                Debug.Log("Entered Play Mode");
                break;
            case PlayModeStateChange.ExitingPlayMode:
                Debug.Log("Exiting Play Mode");
                CleanupDebugTools();
                break;
        }
    }
#endif

    static void SetupDebugCamera() { }
    static void EnableDevelopmentCheats() { }
    static void CleanupDebugTools() { }
}
```

### 5. Analytics and Tracking Initialization

```csharp
using UnityEngine;

public class AnalyticsInitializer
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void InitializeAnalytics()
    {
        // Initialize before any scene loads
        SetupAnalytics();
        RegisterSessionStart();

        // Register for application events
        Application.quitting += OnApplicationQuit;
    }

    static void SetupAnalytics()
    {
        Debug.Log("Analytics SDK initialized");
        // SDK setup code
    }

    static void RegisterSessionStart()
    {
        Debug.Log($"Session started at {System.DateTime.Now}");
        // Track session start
    }

    static void OnApplicationQuit()
    {
        Debug.Log("Session ended");
        // Track session end
    }
}
```

### 6. Service Locator Pattern

```csharp
using UnityEngine;
using System.Collections.Generic;

public class ServiceLocator
{
    private static Dictionary<System.Type, object> services = new Dictionary<System.Type, object>();

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Initialize()
    {
        // Register all services before scenes load
        Register<IDataService>(new PlayerDataService());
        Register<ISaveSystem>(new SaveSystem());
        Register<IInputService>(new InputService());

        Debug.Log($"Registered {services.Count} services");
    }

    public static void Register<T>(T service)
    {
        services[typeof(T)] = service;
    }

    public static T Get<T>()
    {
        if (services.TryGetValue(typeof(T), out object service))
        {
            return (T)service;
        }

        Debug.LogError($"Service {typeof(T)} not found!");
        return default;
    }
}

// Interfaces
public interface IDataService { }
public interface ISaveSystem { }
public interface IInputService { }

// Implementations
public class PlayerDataService : IDataService { }
public class SaveSystem : ISaveSystem { }
public class InputService : IInputService { }
```

### 7. Configuration Loading

```csharp
using UnityEngine;

public class GameConfig
{
    public static GameConfig Instance { get; private set; }

    public int MaxPlayers { get; private set; }
    public float GameSpeed { get; private set; }
    public bool DebugMode { get; private set; }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void LoadConfig()
    {
        Instance = new GameConfig();
        Instance.Load();
    }

    void Load()
    {
        // Load from PlayerPrefs, JSON, ScriptableObject, etc.
        MaxPlayers = PlayerPrefs.GetInt("MaxPlayers", 4);
        GameSpeed = PlayerPrefs.GetFloat("GameSpeed", 1.0f);
        DebugMode = Debug.isDebugBuild;

        Debug.Log($"Config loaded: MaxPlayers={MaxPlayers}, Speed={GameSpeed}");
    }
}

// Usage from anywhere:
public class GameController : MonoBehaviour
{
    void Start()
    {
        int maxPlayers = GameConfig.Instance.MaxPlayers;
        // Config is guaranteed to be loaded
    }
}
```

## Best Practices

### 1. **Use Appropriate Timing**
Choose the right `RuntimeInitializeLoadType` for your needs:
```csharp
// For manager setup that nothing depends on yet
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]

// For accessing scene objects after they're loaded
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]

// For resetting static state (important in editor)
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
```

### 2. **Keep Methods Static and Simple**
```csharp
// ✅ Good
[RuntimeInitializeOnLoadMethod]
static void Initialize()
{
    SetupManagers();
    RegisterCallbacks();
}

// ❌ Bad - instance methods won't work
[RuntimeInitializeOnLoadMethod]
void Initialize()  // Must be static!
{
    // This won't compile
}
```

### 3. **Reset Static State in Editor**
```csharp
public class MyManager
{
    private static MyManager instance;

    // IMPORTANT: Reset static state when domain reloads in editor
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void ResetStatics()
    {
        instance = null;
        // Reset all static fields
    }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Initialize()
    {
        instance = new MyManager();
    }
}
```

### 4. **Don't Depend on Execution Order Between Initializers**
```csharp
// ❌ Dangerous - order not guaranteed between different classes
[RuntimeInitializeOnLoadMethod]
static void InitA() { /* Needs InitB to run first */ }

// Different class
[RuntimeInitializeOnLoadMethod]
static void InitB() { /* Should run before InitA */ }

// ✅ Better - explicit order within one class
[RuntimeInitializeOnLoadMethod]
static void Initialize()
{
    InitB();  // Explicit order
    InitA();
}
```

### 5. **Use for Cross-Scene Concerns Only**
```csharp
// ✅ Good use cases
[RuntimeInitializeOnLoadMethod]
static void InitGlobalSystems()
{
    // Managers that persist across scenes
    // Analytics, input, audio, etc.
}

// ❌ Bad use case
[RuntimeInitializeOnLoadMethod]
static void InitSceneSpecificStuff()
{
    // Don't use for scene-specific setup
    // Use MonoBehaviour Awake/Start instead
}
```

### 6. **Handle Editor vs Build Differences**
```csharp
[RuntimeInitializeOnLoadMethod]
static void Initialize()
{
#if UNITY_EDITOR
    Debug.Log("Running in editor");
    EnableDebugFeatures();
#else
    Debug.Log("Running in build");
    DisableDebugFeatures();
#endif
}
```

### 7. **Clean Up Properly**
```csharp
[RuntimeInitializeOnLoadMethod]
static void Initialize()
{
    SetupSystem();

    // Register cleanup
    Application.quitting += Cleanup;
}

static void Cleanup()
{
    // Release resources
    // Unregister callbacks
    // Save data
}
```

## Common Patterns

### Pattern 1: Persistent Manager GameObject

```csharp
using UnityEngine;

public class GameManagerSpawner
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void SpawnGameManager()
    {
        GameObject managerGO = new GameObject("GameManager");
        managerGO.AddComponent<GameManager>();
        Object.DontDestroyOnLoad(managerGO);

        Debug.Log("Game Manager spawned and made persistent");
    }
}

public class GameManager : MonoBehaviour
{
    void Awake()
    {
        // This GameObject was created automatically
        // No need to place it in scenes manually
    }
}
```

### Pattern 2: Event System Registration

```csharp
using UnityEngine;
using System;

public class EventManager
{
    public static event Action OnGameStart;
    public static event Action OnGameEnd;

    [RuntimeInitializeOnLoadMethod]
    static void Initialize()
    {
        // Auto-register core listeners
        OnGameStart += LogGameStart;
        OnGameEnd += LogGameEnd;

        // Trigger game start
        OnGameStart?.Invoke();
    }

    static void LogGameStart() => Debug.Log("Game Started!");
    static void LogGameEnd() => Debug.Log("Game Ended!");

    // Call this from anywhere when game ends
    public static void TriggerGameEnd() => OnGameEnd?.Invoke();
}
```

### Pattern 3: ScriptableObject Preloading

```csharp
using UnityEngine;

public class GameDatabase
{
    public static ItemDatabase Items { get; private set; }
    public static CharacterDatabase Characters { get; private set; }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void LoadDatabases()
    {
        Items = Resources.Load<ItemDatabase>("GameData/Items");
        Characters = Resources.Load<CharacterDatabase>("GameData/Characters");

        if (Items == null || Characters == null)
        {
            Debug.LogError("Failed to load game databases!");
            return;
        }

        Debug.Log($"Loaded {Items.ItemCount} items, {Characters.CharacterCount} characters");
    }
}
```

### Pattern 4: Input System Configuration

```csharp
using UnityEngine;

public class InputConfiguration
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void ConfigureInput()
    {
        // Set touch simulation for testing on desktop
#if UNITY_EDITOR
        Input.simulateMouseWithTouches = true;
#endif

        // Configure touch sensitivity
        Input.multiTouchEnabled = true;

        // Register input callbacks
        RegisterInputHandlers();

        Debug.Log("Input configured");
    }

    static void RegisterInputHandlers()
    {
        // Setup input event handlers
    }
}
```

## RuntimeInitializeLoadType Timing Chart

```
Application Start
    ↓
AfterAssembliesLoaded       ← First chance to run code
    ↓
SubsystemRegistration       ← Reset static state (editor)
    ↓
BeforeSceneLoad            ← Initialize managers (most common)
    ↓
[Scene Loads]
    ↓
Awake() calls              ← MonoBehaviour Awake
    ↓
OnEnable() calls
    ↓
AfterSceneLoad             ← Access scene objects (default)
    ↓
Start() calls
    ↓
[Game Running]
```

## Technical Details

### How It Works

1. **Attribute Discovery**: Unity scans all assemblies for methods marked with `[RuntimeInitializeOnLoadMethod]`
2. **Execution Queue**: Methods are queued based on their `RuntimeInitializeLoadType`
3. **Automatic Invocation**: Unity calls these methods at the specified times
4. **One-Time Execution**: Each method runs exactly once per application session

### Editor vs Build Behavior

**In Editor**:
- Runs every time you enter Play Mode
- `SubsystemRegistration` helps reset static state between sessions
- `[InitializeOnLoadMethod]` runs when editor loads (not in builds)

**In Builds**:
- Runs once when application launches
- No domain reloading (static state persists)
- `SubsystemRegistration` has no special meaning

### Performance Considerations

```csharp
// ❌ Expensive operations can delay startup
[RuntimeInitializeOnLoadMethod]
static void SlowInitialization()
{
    for (int i = 0; i < 1000000; i++)
    {
        // Heavy computation
    }
}

// ✅ Defer expensive work
[RuntimeInitializeOnLoadMethod]
static void FastInitialization()
{
    // Quick setup only
    CoroutineRunner.StartCoroutine(LoadHeavyResourcesAsync());
}
```

## Alternative: InitializeOnLoad (Editor Only)

```csharp
#if UNITY_EDITOR
using UnityEditor;

[InitializeOnLoad]
public class EditorInitializer
{
    // Static constructor runs when Unity editor loads
    static EditorInitializer()
    {
        Debug.Log("Editor initialized");
        EditorApplication.playModeStateChanged += OnPlayModeChange;
    }

    static void OnPlayModeChange(PlayModeStateChange state)
    {
        // Handle play mode changes
    }
}
#endif
```

## When NOT to Use This Pattern

**Avoid for**:
- Scene-specific initialization (use MonoBehaviour instead)
- UI setup that depends on scene hierarchy
- Level-specific configuration
- Anything that should run multiple times

**Use MonoBehaviour instead when**:
- You need inspector-assignable references
- Initialization depends on scene context
- You need Unity lifecycle methods (Update, etc.)
- Setup is level-specific

## Conclusion

The `[RuntimeInitializeOnLoadMethod]` attribute is one of Unity's most powerful yet underutilized features. It eliminates the need for initialization scenes, manual manager setup, and GameObject dependencies, resulting in cleaner, more maintainable code that "just works" from the moment your application starts.

By combining static methods with this attribute, you ensure critical systems initialize reliably and automatically, without manual intervention. Whether you're setting up managers, registering callbacks, loading configuration, or spawning persistent objects, this pattern provides a robust foundation for application-wide initialization.

Master this pattern, and you'll write initialization code that's impossible to forget, guaranteed to execute, and trivial to test. Your future self will thank you when you can delete all those "remember to drag this prefab into every scene" notes.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

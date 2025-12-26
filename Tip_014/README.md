# #UNITY TIPS 014/100

## Unlocking Inspector Debug Mode - See Everything Under the Hood

<img src="TIP0014.png" alt="Inspector Debug Mode" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

Unity's Inspector typically shows only serialized fields—public variables or those marked with `[SerializeField]`. But what if you need to verify a private property's value at runtime? Or check whether a cached reference is actually being set? Or inspect computed properties without adding debug logs?

Inspector Debug Mode reveals **all** variables in a class: private fields, properties, backing fields, even Unity's internal state. It's an invaluable debugging tool that eliminates guesswork and lets you see exactly what's happening inside your objects—no Debug.Log spam required.

<br clear="left">

## The Problem

During development, you often need to verify internal state:
- Is that cached `Rigidbody` reference actually assigned?
- What's the current value of a private counter?
- Is that auto-property's backing field null?
- What are the internal Unity component values?

The typical approach is littering code with `Debug.Log` statements, recompiling, and checking the console. This workflow is slow, breaks concentration, and clutters your codebase with temporary debugging code.

## The Solution

Right-click the Inspector tab header and toggle between **Normal** and **Debug** mode. Debug mode exposes every field and property in the selected object, including:

- Private fields
- Properties (with their backing fields)
- Protected and internal members
- Unity's internal component data
- Non-serialized public fields

You can also use **Debug-Internal** mode to see even deeper into Unity's internals.

## How to Access Debug Mode

### Method 1: Right-Click Context Menu
1. Right-click the Inspector tab header (the word "Inspector")
2. Select **Debug** from the dropdown menu
3. Toggle back to **Normal** when done

### Method 2: Three-Dot Menu
1. Click the three-dot menu (⋮) in the top-right corner of the Inspector
2. Select **Debug** or **Debug-Internal**

### Method 3: Lock Inspector First
1. Lock the Inspector (click the lock icon)
2. Switch to Debug mode
3. Select different objects while keeping the debug view

## Code Examples

### Example 1: Verifying Cached References

```csharp
using UnityEngine;

public class CachedComponentExample : MonoBehaviour
{
    // Public - visible in Normal mode
    [SerializeField] private float speed = 5f;

    // Private - only visible in Debug mode
    private Rigidbody rb;
    private Transform cachedTransform;
    private bool isInitialized;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        cachedTransform = transform;
        isInitialized = true;
    }

    void Update()
    {
        if (!isInitialized) return;

        float moveInput = Input.GetAxis("Horizontal");
        rb.velocity = cachedTransform.right * moveInput * speed;
    }
}
```

**In Debug Mode**, you can verify at runtime:
- Is `rb` assigned (not null)?
- Is `cachedTransform` pointing to the correct object?
- Did `isInitialized` get set to `true`?

No need for `Debug.Log(rb != null ? "RB found" : "RB is null")`!

### Example 2: Inspecting Properties

```csharp
using UnityEngine;

public class HealthSystem : MonoBehaviour
{
    [SerializeField] private int maxHealth = 100;

    // Property - not visible in Normal mode
    public int CurrentHealth { get; private set; }

    // Computed property - only exists at runtime
    public float HealthPercentage => (float)CurrentHealth / maxHealth;

    // Property with custom logic
    public bool IsAlive => CurrentHealth > 0;

    void Start()
    {
        CurrentHealth = maxHealth;
    }

    public void TakeDamage(int damage)
    {
        CurrentHealth = Mathf.Max(0, CurrentHealth - damage);

        if (!IsAlive)
        {
            Die();
        }
    }

    void Die()
    {
        Debug.Log("Player died!");
    }
}
```

**In Debug Mode**, you'll see:
- `<CurrentHealth>k__BackingField` (the actual backing field)
- The current value of `CurrentHealth` property
- Real-time values of `HealthPercentage` and `IsAlive`

### Example 3: Debugging State Machines

```csharp
using UnityEngine;

public class EnemyAI : MonoBehaviour
{
    public enum AIState { Idle, Patrol, Chase, Attack, Flee }

    [SerializeField] private Transform player;
    [SerializeField] private float detectionRadius = 10f;
    [SerializeField] private float attackRange = 2f;

    // Private state - only visible in Debug mode
    private AIState currentState = AIState.Idle;
    private AIState previousState;
    private float stateTimer;
    private Vector3 lastKnownPlayerPosition;
    private bool playerDetected;

    void Update()
    {
        float distanceToPlayer = Vector3.Distance(transform.position, player.position);
        playerDetected = distanceToPlayer <= detectionRadius;

        UpdateState(distanceToPlayer);
        stateTimer += Time.deltaTime;
    }

    void UpdateState(float distanceToPlayer)
    {
        previousState = currentState;

        if (!playerDetected)
        {
            currentState = AIState.Patrol;
        }
        else if (distanceToPlayer <= attackRange)
        {
            currentState = AIState.Attack;
        }
        else
        {
            currentState = AIState.Chase;
            lastKnownPlayerPosition = player.position;
        }

        if (currentState != previousState)
        {
            stateTimer = 0f; // Reset timer on state change
        }
    }
}
```

**In Debug Mode**, monitor:
- `currentState` and `previousState` enum values
- `stateTimer` incrementing in real-time
- `lastKnownPlayerPosition` coordinates
- `playerDetected` boolean flag

Perfect for debugging AI behavior without console spam!

### Example 4: Tracking Animation States

```csharp
using UnityEngine;

public class CharacterAnimator : MonoBehaviour
{
    [SerializeField] private Animator animator;

    private int currentAnimationHash;
    private string currentAnimationName;
    private float normalizedTime;
    private bool isTransitioning;

    // Animation parameter hashes (cached for performance)
    private readonly int speedHash = Animator.StringToHash("Speed");
    private readonly int jumpHash = Animator.StringToHash("Jump");
    private readonly int groundedHash = Animator.StringToHash("Grounded");

    void Update()
    {
        AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);

        currentAnimationHash = stateInfo.shortNameHash;
        currentAnimationName = animator.GetCurrentAnimatorClipInfo(0)[0].clip.name;
        normalizedTime = stateInfo.normalizedTime;
        isTransitioning = animator.IsInTransition(0);

        // Update parameters
        float speed = GetComponent<Rigidbody>().velocity.magnitude;
        animator.SetFloat(speedHash, speed);
    }

    public void Jump()
    {
        animator.SetTrigger(jumpHash);
    }
}
```

**In Debug Mode**, you see:
- `currentAnimationHash` and `currentAnimationName`
- `normalizedTime` progressing from 0.0 to 1.0
- `isTransitioning` boolean state
- Parameter hashes (`speedHash`, `jumpHash`, `groundedHash`)

### Example 5: Monitoring Object Pools

```csharp
using UnityEngine;
using System.Collections.Generic;

public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int initialPoolSize = 20;

    // Private - only visible in Debug mode
    private Queue<GameObject> availableObjects = new Queue<GameObject>();
    private List<GameObject> allObjects = new List<GameObject>();
    private int totalCreated;
    private int activeCount;
    private int availableCount;

    void Start()
    {
        for (int i = 0; i < initialPoolSize; i++)
        {
            CreateNewObject();
        }
    }

    GameObject CreateNewObject()
    {
        GameObject obj = Instantiate(prefab);
        obj.SetActive(false);
        allObjects.Add(obj);
        availableObjects.Enqueue(obj);
        totalCreated++;
        UpdateCounts();
        return obj;
    }

    public GameObject Get()
    {
        GameObject obj = availableObjects.Count > 0
            ? availableObjects.Dequeue()
            : CreateNewObject();

        obj.SetActive(true);
        UpdateCounts();
        return obj;
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        availableObjects.Enqueue(obj);
        UpdateCounts();
    }

    void UpdateCounts()
    {
        availableCount = availableObjects.Count;
        activeCount = totalCreated - availableCount;
    }
}
```

**In Debug Mode**, monitor pool statistics:
- `totalCreated` - total objects instantiated
- `activeCount` - currently active objects
- `availableCount` - objects available in pool
- `availableObjects` queue size
- `allObjects` list contents

### Example 6: Verifying Singleton Initialization

```csharp
using UnityEngine;

public class GameManager : MonoBehaviour
{
    // Public static - visible in Debug mode on the class
    private static GameManager instance;

    public static GameManager Instance
    {
        get
        {
            if (instance == null)
            {
                instance = FindObjectOfType<GameManager>();
            }
            return instance;
        }
    }

    // Private game state
    private int score;
    private int level = 1;
    private float gameTime;
    private bool isPaused;
    private bool isGameOver;

    void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        DontDestroyOnLoad(gameObject);
    }

    void Update()
    {
        if (!isPaused && !isGameOver)
        {
            gameTime += Time.deltaTime;
        }
    }

    public void AddScore(int points)
    {
        score += points;
    }

    public void PauseGame()
    {
        isPaused = true;
        Time.timeScale = 0f;
    }

    public void ResumeGame()
    {
        isPaused = false;
        Time.timeScale = 1f;
    }
}
```

**In Debug Mode**, verify:
- `instance` static field is properly assigned
- `score`, `level`, `gameTime` values
- `isPaused` and `isGameOver` flags
- All private game state at a glance

### Example 7: Debugging Coroutine State

```csharp
using UnityEngine;
using System.Collections;

public class SpawnManager : MonoBehaviour
{
    [SerializeField] private GameObject enemyPrefab;
    [SerializeField] private float spawnInterval = 2f;

    private Coroutine spawnCoroutine;
    private int enemiesSpawned;
    private float timeSinceLastSpawn;
    private bool isSpawning;

    void Start()
    {
        StartSpawning();
    }

    public void StartSpawning()
    {
        if (spawnCoroutine == null)
        {
            spawnCoroutine = StartCoroutine(SpawnRoutine());
            isSpawning = true;
        }
    }

    public void StopSpawning()
    {
        if (spawnCoroutine != null)
        {
            StopCoroutine(spawnCoroutine);
            spawnCoroutine = null;
            isSpawning = false;
        }
    }

    IEnumerator SpawnRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(spawnInterval);

            Vector3 spawnPos = Random.insideUnitSphere * 10f;
            spawnPos.y = 0;
            Instantiate(enemyPrefab, spawnPos, Quaternion.identity);

            enemiesSpawned++;
            timeSinceLastSpawn = 0f;
        }
    }

    void Update()
    {
        if (isSpawning)
        {
            timeSinceLastSpawn += Time.deltaTime;
        }
    }
}
```

**In Debug Mode**, track:
- `spawnCoroutine` reference (null or active)
- `enemiesSpawned` counter
- `timeSinceLastSpawn` incrementing
- `isSpawning` flag state

## Best Practices

### 1. **Use Debug Mode During Development, Not Production**
Debug mode is a development tool. Don't rely on it for production debugging—use proper logging and profiling tools instead.

### 2. **Lock the Inspector for Focused Debugging**
When debugging a specific object, lock the Inspector (lock icon) before switching to Debug mode. This lets you select other objects in the hierarchy while keeping the debug view focused.

### 3. **Combine with Play Mode Pause**
Pause the game (`Ctrl/Cmd + Shift + P`) while in Debug mode to inspect exact state at a specific moment.

### 4. **Remember to Switch Back to Normal Mode**
Debug mode shows **everything**, which can be overwhelming. Switch back to Normal mode when you're done debugging to avoid clutter.

### 5. **Use Debug-Internal for Unity Internals**
If you need to see Unity's internal component data (like `Transform.m_LocalPosition`), use **Debug-Internal** mode. Be careful modifying these values!

### 6. **Name Private Fields Descriptively**
Since you'll see them in Debug mode, use clear names:

```csharp
// Good
private float currentSpeed;
private bool isGrounded;

// Avoid
private float s;
private bool b1;
```

### 7. **Combine with Gizmos for Visual Debugging**
Use Debug mode to verify values, then visualize them with Gizmos:

```csharp
void OnDrawGizmosSelected()
{
    if (playerDetected)
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, detectionRadius);
    }
}
```

### 8. **Watch for Backing Fields**
Properties show their backing fields with names like `<PropertyName>k__BackingField`. This is normal C# compiler behavior.

## Common Use Cases

### Use Case 1: Debugging Null References
Instantly verify which cached component references are null without adding debug logs:

```csharp
private Rigidbody rb;         // Is this null?
private AudioSource audio;    // Is this assigned?
private Transform target;     // Does this point to the right object?
```

### Use Case 2: Monitoring State Transitions
Watch state machines and FSMs update in real-time without console spam.

### Use Case 3: Verifying Initialization Order
Check that `Awake()` and `Start()` methods properly initialized all private fields.

### Use Case 4: Tracking Performance Counters
Monitor private counters, timers, and statistics during play mode.

### Use Case 5: Inspecting Unity Component Internals
See internal Unity data like `Transform` matrices, `Rigidbody` velocity vectors, or `Animator` state hashes.

## Limitations to Be Aware Of

### 1. **Read-Only Properties Are Not Editable**
Properties with only a getter can't be modified in the Inspector, even in Debug mode:

```csharp
public float HealthPercentage => currentHealth / maxHealth; // Read-only
```

### 2. **Methods Don't Appear**
Debug mode shows fields and properties, but not methods. Use the console for method debugging.

### 3. **Performance Impact**
Debug mode refreshes all visible values every frame. For very large scripts with hundreds of fields, this can impact editor performance slightly.

### 4. **No Serialization of Private Fields**
Debug mode lets you **see** private fields, but changes aren't saved between play sessions (unless marked `[SerializeField]`).

## Debug Mode vs. Normal Mode Comparison

| Feature | Normal Mode | Debug Mode | Debug-Internal |
|---------|-------------|------------|----------------|
| Public serialized fields | ✅ | ✅ | ✅ |
| Private `[SerializeField]` fields | ✅ | ✅ | ✅ |
| Private fields | ❌ | ✅ | ✅ |
| Properties | ❌ | ✅ | ✅ |
| Backing fields | ❌ | ✅ | ✅ |
| Unity internals | ❌ | ❌ | ✅ |

## Keyboard Shortcuts for Faster Debugging

While there's no direct shortcut to toggle Debug mode, you can speed up your workflow:

1. **Lock Inspector**: `Ctrl/Cmd + Click` the lock icon
2. **Pause Play Mode**: `Ctrl/Cmd + Shift + P`
3. **Step Frame**: `Ctrl/Cmd + Alt + P`
4. **Multiple Inspectors**: Right-click Inspector tab → Add Tab → Inspector

## Advanced Workflow: Multi-Inspector Debug Setup

For complex debugging, use multiple Inspector windows:

1. **Inspector 1**: Normal mode (locked on GameObject A)
2. **Inspector 2**: Debug mode (locked on GameObject B)
3. **Inspector 3**: Normal mode (free to select)

This lets you compare normal vs. debug views simultaneously or monitor multiple objects.

## Conclusion

Inspector Debug Mode is one of Unity's most underutilized features. It eliminates the need for temporary `Debug.Log` statements, provides real-time insight into object state, and makes debugging internal logic effortless.

Right-click the Inspector tab, toggle Debug mode, and see everything your scripts are doing under the hood. It's a simple workflow change that dramatically improves your debugging efficiency and helps you understand exactly what's happening in your game at runtime.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

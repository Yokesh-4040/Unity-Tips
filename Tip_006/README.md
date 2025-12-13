# #UNITY TIPS 006/100

## Leveraging Transform.hasChanged for Efficient State Tracking

Unity's `Transform` component includes a built-in property called `hasChanged` that automatically tracks whether a transform has been modified. This simple boolean flag provides an efficient way to detect movement, rotation, or scale changes without manually comparing transform values every frame. Understanding and utilizing `hasChanged` can significantly optimize your code and simplify common gameplay patterns.

## The Problem

Detecting when GameObjects move, rotate, or scale is a common requirement in game development. Traditional approaches often involve:

- Storing previous transform values and comparing them each frame
- Unnecessary calculations even when objects haven't moved
- Complex change detection logic scattered throughout your codebase
- Performance overhead from continuous value comparisons

```csharp
// Traditional approach - inefficient
private Vector3 lastPosition;
private Quaternion lastRotation;
private Vector3 lastScale;

void Update()
{
    if (transform.position != lastPosition ||
        transform.rotation != lastRotation ||
        transform.localScale != lastScale)
    {
        OnTransformChanged();
        lastPosition = transform.position;
        lastRotation = transform.rotation;
        lastScale = transform.localScale;
    }
}
```

This approach is verbose, error-prone, and wastes memory storing redundant data that Unity already tracks internally.

## The Solution: Transform.hasChanged

Unity's `Transform.hasChanged` is a public boolean property that automatically gets set to `true` whenever the transform's position, rotation, or scale changes. This built-in flag eliminates the need for manual tracking and provides a clean, efficient way to detect transform modifications.

### Key Characteristics

- **Automatic Detection**: Unity sets it to `true` when position, rotation, or scale changes
- **Manual Reset Required**: You must manually set it back to `false` after handling the change
- **Lightweight**: No performance overhead - Unity maintains this flag internally anyway
- **Persistent**: Stays `true` until you explicitly reset it

## Code Examples

### Example 1: Basic Transform Change Detection

```csharp
using UnityEngine;

public class TransformMonitor : MonoBehaviour
{
    void Update()
    {
        if (transform.hasChanged)
        {
            Debug.Log($"{gameObject.name} transform has changed!");
            Debug.Log($"Position: {transform.position}");
            Debug.Log($"Rotation: {transform.rotation.eulerAngles}");
            Debug.Log($"Scale: {transform.localScale}");

            // Reset the flag after handling the change
            transform.hasChanged = false;
        }
    }
}
```

### Example 2: Update UI When Player Moves

```csharp
using UnityEngine;
using UnityEngine.UI;

public class PlayerPositionUI : MonoBehaviour
{
    [SerializeField] private Transform playerTransform;
    [SerializeField] private Text positionText;

    void LateUpdate()
    {
        // Only update UI when player actually moves
        if (playerTransform.hasChanged)
        {
            Vector3 pos = playerTransform.position;
            positionText.text = $"Position: ({pos.x:F2}, {pos.y:F2}, {pos.z:F2})";

            playerTransform.hasChanged = false;
        }
    }
}
```

### Example 3: Dirty Flag Pattern for Expensive Calculations

```csharp
using UnityEngine;

public class ShadowProjector : MonoBehaviour
{
    [SerializeField] private Transform trackedObject;
    [SerializeField] private LayerMask groundLayer;
    private Vector3 projectedShadowPosition;

    void Update()
    {
        // Only recalculate shadow projection when object moves
        if (trackedObject.hasChanged)
        {
            RecalculateShadowProjection();
            trackedObject.hasChanged = false;
        }

        // Render shadow at cached position
        RenderShadow(projectedShadowPosition);
    }

    void RecalculateShadowProjection()
    {
        // Expensive raycast operation - only do when necessary
        if (Physics.Raycast(trackedObject.position, Vector3.down, out RaycastHit hit, 100f, groundLayer))
        {
            projectedShadowPosition = hit.point;
        }
    }

    void RenderShadow(Vector3 position)
    {
        // Render shadow mesh or decal at position
    }
}
```

### Example 4: Network Synchronization Optimization

```csharp
using UnityEngine;
using UnityEngine.Networking;

public class NetworkTransformOptimized : MonoBehaviour
{
    [SerializeField] private Transform syncedTransform;
    [SerializeField] private float syncInterval = 0.1f;
    private float lastSyncTime;

    void Update()
    {
        // Only send network updates when transform actually changed
        if (syncedTransform.hasChanged && Time.time - lastSyncTime >= syncInterval)
        {
            SendTransformUpdate();
            syncedTransform.hasChanged = false;
            lastSyncTime = Time.time;
        }
    }

    void SendTransformUpdate()
    {
        // Send position, rotation, scale to network
        Debug.Log("Sending transform data to network...");
        // NetworkSend(transform.position, transform.rotation, transform.localScale);
    }
}
```

### Example 5: Object Pooling Reset Detection

```csharp
using UnityEngine;
using System.Collections.Generic;

public class PooledObjectManager : MonoBehaviour
{
    private List<GameObject> pooledObjects = new List<GameObject>();

    public GameObject GetPooledObject()
    {
        foreach (GameObject obj in pooledObjects)
        {
            if (!obj.activeInHierarchy)
            {
                // Reset transform changed flag when recycling objects
                obj.transform.hasChanged = false;
                return obj;
            }
        }
        return CreateNewPooledObject();
    }

    public void ReturnToPool(GameObject obj)
    {
        obj.SetActive(false);

        // Check if object was modified during its lifetime
        if (obj.transform.hasChanged)
        {
            Debug.Log($"{obj.name} was modified - resetting transform");
            obj.transform.localPosition = Vector3.zero;
            obj.transform.localRotation = Quaternion.identity;
            obj.transform.localScale = Vector3.one;
            obj.transform.hasChanged = false;
        }
    }

    GameObject CreateNewPooledObject()
    {
        GameObject newObj = new GameObject("PooledObject");
        pooledObjects.Add(newObj);
        return newObj;
    }
}
```

### Example 6: Camera Follow with Change Detection

```csharp
using UnityEngine;

public class CameraFollowOptimized : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private Vector3 offset = new Vector3(0, 5, -10);
    [SerializeField] private float smoothSpeed = 0.125f;

    void LateUpdate()
    {
        // Only update camera when target moves
        if (target.hasChanged)
        {
            Vector3 desiredPosition = target.position + offset;
            Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);
            transform.position = smoothedPosition;
            transform.LookAt(target);

            target.hasChanged = false;
        }
    }
}
```

### Example 7: Hierarchical Change Detection

```csharp
using UnityEngine;

public class HierarchyChangeTracker : MonoBehaviour
{
    void Update()
    {
        CheckHierarchyChanges(transform);
    }

    void CheckHierarchyChanges(Transform parent)
    {
        // Check if this transform changed
        if (parent.hasChanged)
        {
            Debug.Log($"{parent.name} has changed");
            HandleTransformChange(parent);
            parent.hasChanged = false;
        }

        // Recursively check all children
        foreach (Transform child in parent)
        {
            CheckHierarchyChanges(child);
        }
    }

    void HandleTransformChange(Transform t)
    {
        // Update spatial hash, octree, or other data structures
        Debug.Log($"Updating data structures for {t.name}");
    }
}
```

## Best Practices

1. **Always Reset the Flag**: After detecting and handling a change, always set `hasChanged` back to `false`. Forgetting this will cause your change-detection code to trigger every frame, defeating the purpose.

2. **Use LateUpdate for UI Updates**: When updating UI based on transform changes, use `LateUpdate()` to ensure you're reading the final transform state after all movement has been applied in `Update()`.

3. **Combine with Throttling**: For expensive operations, combine `hasChanged` with time-based throttling to prevent excessive calculations even if the object moves frequently.

4. **Check at the Right Frequency**: You don't always need to check `hasChanged` every frame. For less critical systems, check every few frames or use coroutines to reduce overhead.

5. **Use for Optimization, Not Core Logic**: `hasChanged` is perfect for optimization (skipping unnecessary work), but don't rely on it for critical gameplay logic that must execute reliably.

6. **Be Aware of Parenting**: Changes to a parent transform will set its `hasChanged` flag, but not necessarily the children's flags. If you need to detect hierarchical changes, check both parent and children.

7. **Reset in OnEnable/OnDisable**: When objects are pooled or reactivated, ensure `hasChanged` is reset to a known state in `OnEnable()` to avoid stale data.

## Common Patterns

### Pattern 1: Dirty Flag Pattern

```csharp
// Only recalculate when data is "dirty" (changed)
if (transform.hasChanged)
{
    RecalculateExpensiveOperation();
    transform.hasChanged = false;
}
```

### Pattern 2: Event-Driven Updates

```csharp
public class TransformEventBroadcaster : MonoBehaviour
{
    public event System.Action OnTransformModified;

    void Update()
    {
        if (transform.hasChanged)
        {
            OnTransformModified?.Invoke();
            transform.hasChanged = false;
        }
    }
}
```

### Pattern 3: Batched Updates

```csharp
private List<Transform> trackedTransforms = new List<Transform>();

void Update()
{
    bool anyChanged = false;

    foreach (Transform t in trackedTransforms)
    {
        if (t.hasChanged)
        {
            anyChanged = true;
            t.hasChanged = false;
        }
    }

    if (anyChanged)
    {
        RebuildSpatialDataStructure();
    }
}
```

### Pattern 4: Conditional Network Sync

```csharp
// Only sync to network when object actually moved
if (transform.hasChanged && ShouldSyncNow())
{
    SyncToNetwork();
    transform.hasChanged = false;
}
```

## Technical Details

### What Triggers hasChanged?

The `hasChanged` flag is set to `true` when any of the following occur:

- `transform.position` is modified
- `transform.rotation` is modified
- `transform.localPosition` is modified
- `transform.localRotation` is modified
- `transform.localScale` is modified
- `transform.SetPositionAndRotation()` is called
- Parent transform changes (affects world position/rotation)

### What Does NOT Trigger hasChanged?

- Reading transform properties (only writes trigger it)
- Changes to child transforms (only the child's flag is set)
- Setting transform to the same value it already has (Unity optimizes this)

### Performance Characteristics

- **Read Cost**: Near-zero - simple boolean check
- **Write Cost**: Near-zero - simple boolean assignment
- **Memory Cost**: Negligible - single boolean per transform
- **Unity Overhead**: None - Unity maintains this flag for internal use anyway

### Internal Implementation

Unity uses `hasChanged` internally for its own optimization purposes. When you set it to `false`, you're not interfering with Unity's systems - you're simply resetting the user-facing flag. Unity's internal transform change detection continues to work normally.

### Thread Safety

`Transform.hasChanged` is not thread-safe. It should only be accessed from the main Unity thread. Do not read or write this property from worker threads or jobs.

## Conclusion

`Transform.hasChanged` is a simple yet powerful tool that leverages Unity's internal transform tracking to optimize your code. By eliminating manual change detection and enabling efficient dirty-flag patterns, this property helps you write cleaner, more performant code.

The key to effectively using `hasChanged` is understanding that it's a manual-reset flag: Unity sets it to `true` automatically, but you must reset it to `false` after handling the change. This design gives you complete control over when and how you respond to transform modifications.

Whether you're optimizing UI updates, reducing network traffic, or avoiding expensive calculations, `hasChanged` should be part of your Unity optimization toolkit. It's a zero-cost abstraction that makes your code more efficient and easier to read.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

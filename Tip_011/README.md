# #UNITY TIPS 011/100

## Mastering the Dirty Flag Pattern - Ensuring Your Changes Persist

Have you ever made changes to an object in the Unity Editor through a script, only to find those changes mysteriously vanish after a domain reload or when you exit Play Mode? You're not alone. Unity's serialization system needs explicit signals when data has been modified outside of the standard Inspector workflow. This is where the "dirty flag" pattern becomes essential.

Understanding and properly using dirty flags is fundamental to writing reliable Editor tools and custom inspectors. Without marking objects as dirty, Unity assumes nothing has changed, and your modifications might never be saved to disk. This seemingly simple concept is the difference between robust Editor extensions and frustrating, unpredictable tools.

## The Problem

Unity's serialization system is optimized for performance. It doesn't constantly monitor every object for changes - that would be computationally expensive. Instead, Unity relies on a "dirty flag" system:

```csharp
// This change happens in code, but Unity doesn't know about it
public class MaterialRandomizer : MonoBehaviour
{
    void RandomizeColors()
    {
        Renderer renderer = GetComponent<Renderer>();
        renderer.sharedMaterial.color = new Color(
            Random.value,
            Random.value,
            Random.value
        );
        // Unity doesn't know this material asset was modified!
        // Changes may not be saved
    }
}
```

When you modify objects through the Inspector, Unity automatically marks them as dirty. But when you modify them through scripts (especially Editor scripts), you must explicitly tell Unity that something changed.

## The Solution: EditorUtility.SetDirty()

The `EditorUtility.SetDirty()` method explicitly marks an object as modified, ensuring Unity saves the changes:

```csharp
#if UNITY_EDITOR
using UnityEditor;
#endif

public class MaterialRandomizer : MonoBehaviour
{
    void RandomizeColors()
    {
        Renderer renderer = GetComponent<Renderer>();
        renderer.sharedMaterial.color = new Color(
            Random.value,
            Random.value,
            Random.value
        );

        #if UNITY_EDITOR
        EditorUtility.SetDirty(renderer.sharedMaterial);
        #endif
    }
}
```

## Core Usage Patterns

### 1. Modifying ScriptableObject Assets

```csharp
#if UNITY_EDITOR
using UnityEditor;
#endif

[CreateAssetMenu(fileName = "GameConfig", menuName = "Game/Config")]
public class GameConfig : ScriptableObject
{
    public int maxPlayers = 4;
    public float spawnDelay = 2f;

    public void UpdateMaxPlayers(int newMax)
    {
        maxPlayers = newMax;

        #if UNITY_EDITOR
        EditorUtility.SetDirty(this);
        #endif
    }
}
```

### 2. Custom Editor with Dirty Tracking

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(EnemySpawner))]
public class EnemySpawnerEditor : Editor
{
    public override void OnInspectorGUI()
    {
        EnemySpawner spawner = (EnemySpawner)target;

        EditorGUI.BeginChangeCheck();

        spawner.spawnRate = EditorGUILayout.FloatField("Spawn Rate", spawner.spawnRate);
        spawner.maxEnemies = EditorGUILayout.IntField("Max Enemies", spawner.maxEnemies);

        if (EditorGUI.EndChangeCheck())
        {
            EditorUtility.SetDirty(spawner);
        }

        if (GUILayout.Button("Randomize Spawn Points"))
        {
            spawner.RandomizeSpawnPoints();
            EditorUtility.SetDirty(spawner);
        }
    }
}
```

### 3. Modifying Prefab Assets

```csharp
using UnityEngine;
using UnityEditor;

public class PrefabModifier : EditorWindow
{
    [MenuItem("Tools/Modify Player Prefab")]
    static void ModifyPlayerPrefab()
    {
        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(
            "Assets/Prefabs/Player.prefab"
        );

        if (prefab != null)
        {
            PlayerController controller = prefab.GetComponent<PlayerController>();
            controller.moveSpeed = 10f;
            controller.jumpForce = 15f;

            EditorUtility.SetDirty(prefab);
            AssetDatabase.SaveAssets();
        }
    }
}
```

### 4. Scene Object Modifications

```csharp
using UnityEngine;
using UnityEditor;

public class LevelDesignTools : EditorWindow
{
    [MenuItem("Tools/Align Selected Objects to Grid")]
    static void AlignToGrid()
    {
        foreach (GameObject obj in Selection.gameObjects)
        {
            Vector3 pos = obj.transform.position;
            obj.transform.position = new Vector3(
                Mathf.Round(pos.x),
                Mathf.Round(pos.y),
                Mathf.Round(pos.z)
            );

            EditorUtility.SetDirty(obj);
        }

        // Mark the scene as dirty so Unity prompts to save
        UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(
            UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene()
        );
    }
}
```

### 5. Batch Asset Processing

```csharp
using UnityEngine;
using UnityEditor;

public class TextureProcessor : EditorWindow
{
    [MenuItem("Tools/Process All Textures")]
    static void ProcessTextures()
    {
        string[] guids = AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/Textures" });

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;

            if (importer != null)
            {
                importer.textureCompression = TextureImporterCompression.Compressed;
                importer.maxTextureSize = 2048;

                EditorUtility.SetDirty(importer);
            }
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }
}
```

## Modern Alternatives and Best Practices

### Using Undo System (Recommended for Editor Tools)

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(WaypointPath))]
public class WaypointPathEditor : Editor
{
    public override void OnInspectorGUI()
    {
        WaypointPath path = (WaypointPath)target;

        if (GUILayout.Button("Add Waypoint"))
        {
            // Undo.RecordObject automatically marks the object as dirty
            Undo.RecordObject(path, "Add Waypoint");
            path.AddWaypoint(Vector3.zero);
        }
    }
}
```

### Using SerializedObject (Preferred for Custom Inspectors)

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(InventorySystem))]
public class InventorySystemEditor : Editor
{
    SerializedProperty maxSlots;
    SerializedProperty startingItems;

    void OnEnable()
    {
        maxSlots = serializedObject.FindProperty("maxSlots");
        startingItems = serializedObject.FindProperty("startingItems");
    }

    public override void OnInspectorGUI()
    {
        // Update reads current values from target object
        serializedObject.Update();

        EditorGUILayout.PropertyField(maxSlots);
        EditorGUILayout.PropertyField(startingItems);

        // ApplyModifiedProperties automatically handles SetDirty
        serializedObject.ApplyModifiedProperties();
    }
}
```

### PrefabUtility for Prefab Modifications

```csharp
using UnityEngine;
using UnityEditor;

public class PrefabBatchEditor : EditorWindow
{
    [MenuItem("Tools/Update All Enemy Prefabs")]
    static void UpdateEnemyPrefabs()
    {
        string[] prefabGuids = AssetDatabase.FindAssets("t:Prefab", new[] { "Assets/Prefabs/Enemies" });

        foreach (string guid in prefabGuids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);

            // Load prefab contents for editing
            using (var editingScope = new PrefabUtility.EditPrefabContentsScope(path))
            {
                GameObject root = editingScope.prefabContentsRoot;
                EnemyController enemy = root.GetComponent<EnemyController>();

                if (enemy != null)
                {
                    enemy.health = 100f;
                    enemy.damage = 10f;
                }
                // Changes are automatically saved when scope is disposed
            }
        }

        AssetDatabase.SaveAssets();
    }
}
```

## Best Practices

### 1. **Mark the Right Object**
Always mark the actual asset being modified, not a component or temporary reference:
```csharp
// ❌ Wrong - marking a component
EditorUtility.SetDirty(gameObject.GetComponent<Renderer>());

// ✅ Correct - marking the material asset
EditorUtility.SetDirty(gameObject.GetComponent<Renderer>().sharedMaterial);
```

### 2. **Combine with AssetDatabase.SaveAssets()**
For critical changes, explicitly save after marking dirty:
```csharp
EditorUtility.SetDirty(myAsset);
AssetDatabase.SaveAssets();
```

### 3. **Use Undo.RecordObject for User-Facing Tools**
This provides both undo functionality AND automatic dirty marking:
```csharp
Undo.RecordObject(target, "Descriptive Action Name");
// Make changes
target.someValue = newValue;
```

### 4. **Prefer SerializedObject in Custom Inspectors**
It handles dirty tracking, multi-object editing, and undo automatically:
```csharp
serializedObject.Update();
// Make changes through SerializedProperty
serializedObject.ApplyModifiedProperties(); // Handles SetDirty automatically
```

### 5. **Mark Scenes Dirty for Transform Changes**
When modifying scene objects, mark the scene itself:
```csharp
EditorUtility.SetDirty(gameObject);
EditorSceneManager.MarkSceneDirty(gameObject.scene);
```

### 6. **Don't Overuse in Runtime Code**
SetDirty is primarily for Editor scripts. Runtime changes don't need dirty marking:
```csharp
// ❌ Unnecessary in runtime MonoBehaviour
void Update()
{
    transform.position += Vector3.forward * Time.deltaTime;
    EditorUtility.SetDirty(this); // Don't do this!
}
```

### 7. **Use Conditional Compilation**
Wrap Editor-only code properly:
```csharp
#if UNITY_EDITOR
using UnityEditor;
#endif

public void ModifyData()
{
    // Make changes

    #if UNITY_EDITOR
    EditorUtility.SetDirty(this);
    #endif
}
```

## Common Patterns

### Pattern 1: Editor Window with Batch Operations
```csharp
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;

public class AudioClipNormalizer : EditorWindow
{
    [MenuItem("Tools/Normalize Audio Clips")]
    static void ShowWindow()
    {
        GetWindow<AudioClipNormalizer>("Audio Normalizer");
    }

    void OnGUI()
    {
        if (GUILayout.Button("Normalize All Audio Clips"))
        {
            NormalizeAudioClips();
        }
    }

    void NormalizeAudioClips()
    {
        string[] guids = AssetDatabase.FindAssets("t:AudioClip");
        int processedCount = 0;

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            AudioImporter importer = AssetImporter.GetAtPath(path) as AudioImporter;

            if (importer != null)
            {
                AudioImporterSampleSettings settings = importer.defaultSampleSettings;
                settings.loadType = AudioClipLoadType.DecompressOnLoad;
                settings.compressionFormat = AudioCompressionFormat.Vorbis;
                settings.quality = 0.7f;

                importer.defaultSampleSettings = settings;
                EditorUtility.SetDirty(importer);
                processedCount++;
            }
        }

        AssetDatabase.SaveAssets();
        Debug.Log($"Normalized {processedCount} audio clips");
    }
}
```

### Pattern 2: PropertyDrawer with Custom Logic
```csharp
using UnityEngine;
using UnityEditor;

[System.Serializable]
public class MinMaxRange
{
    public float min;
    public float max;
}

[CustomPropertyDrawer(typeof(MinMaxRange))]
public class MinMaxRangeDrawer : PropertyDrawer
{
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        SerializedProperty minProp = property.FindPropertyRelative("min");
        SerializedProperty maxProp = property.FindPropertyRelative("max");

        EditorGUI.BeginProperty(position, label, property);

        position = EditorGUI.PrefixLabel(position, GUIUtility.GetControlID(FocusType.Passive), label);

        float minValue = minProp.floatValue;
        float maxValue = maxProp.floatValue;

        Rect minRect = new Rect(position.x, position.y, position.width * 0.45f, position.height);
        Rect maxRect = new Rect(position.x + position.width * 0.55f, position.y, position.width * 0.45f, position.height);

        EditorGUI.BeginChangeCheck();
        minValue = EditorGUI.FloatField(minRect, minValue);
        maxValue = EditorGUI.FloatField(maxRect, maxValue);

        if (EditorGUI.EndChangeCheck())
        {
            minProp.floatValue = Mathf.Min(minValue, maxValue);
            maxProp.floatValue = Mathf.Max(minValue, maxValue);
            property.serializedObject.ApplyModifiedProperties();
        }

        EditorGUI.EndProperty();
    }
}
```

### Pattern 3: Context Menu Actions
```csharp
using UnityEngine;
using UnityEditor;

public class MeshOptimizer : MonoBehaviour
{
    [ContextMenu("Optimize Mesh")]
    void OptimizeMesh()
    {
        MeshFilter meshFilter = GetComponent<MeshFilter>();
        if (meshFilter != null && meshFilter.sharedMesh != null)
        {
            Mesh mesh = meshFilter.sharedMesh;
            mesh.Optimize();
            mesh.RecalculateBounds();

            #if UNITY_EDITOR
            EditorUtility.SetDirty(mesh);
            AssetDatabase.SaveAssets();
            Debug.Log($"Optimized mesh: {mesh.name}");
            #endif
        }
    }

    [MenuItem("GameObject/Optimize Selected Meshes", false, 0)]
    static void OptimizeSelectedMeshes()
    {
        foreach (GameObject obj in Selection.gameObjects)
        {
            MeshFilter filter = obj.GetComponent<MeshFilter>();
            if (filter != null && filter.sharedMesh != null)
            {
                Mesh mesh = filter.sharedMesh;
                mesh.Optimize();
                EditorUtility.SetDirty(mesh);
            }
        }

        AssetDatabase.SaveAssets();
    }
}
```

## Technical Deep Dive

### How Unity's Dirty Flag System Works

Unity's serialization system operates in distinct phases:

1. **Serialization Phase**: Unity scans all objects marked as "dirty"
2. **Write Phase**: Only dirty objects are written to disk
3. **Reset Phase**: Dirty flags are cleared after successful serialization

When you call `EditorUtility.SetDirty()`:
- Unity adds the object to an internal "modified objects" collection
- During the next serialization pass, Unity serializes only these objects
- The change is written to the asset file (.asset, .prefab, .unity, etc.)

### Why Runtime Code Doesn't Need SetDirty

In Play Mode and builds:
- Scene serialization happens during scene saves/loads
- Component values are automatically serialized as part of scene data
- SetDirty is irrelevant because you're not saving asset files during gameplay

### Modern Unity Workflow

Unity has evolved its APIs:

**Legacy (Pre-Unity 5.3)**
```csharp
EditorUtility.SetDirty(obj);
```

**Modern (Unity 2018+)**
```csharp
// For undo-aware changes
Undo.RecordObject(obj, "Action Name");

// For SerializedProperty changes
serializedObject.ApplyModifiedProperties();

// For prefab edits
PrefabUtility.EditPrefabContentsScope();
```

The newer APIs handle dirty marking automatically while providing additional benefits like undo support and better prefab workflows.

## When SetDirty is Still Essential

Despite modern alternatives, `EditorUtility.SetDirty()` remains critical for:

1. **Direct asset modification** outside of SerializedObject
2. **Programmatic batch processing** of assets
3. **Legacy code compatibility**
4. **Non-UnityEngine.Object modifications** where Undo doesn't apply

## Conclusion

The dirty flag pattern is a cornerstone of Unity's Editor scripting architecture. While modern APIs like `Undo.RecordObject()` and `SerializedObject` have reduced the need for explicit `SetDirty()` calls, understanding when and how to use it remains essential for any Unity developer building Editor tools.

Remember: Unity doesn't track every change automatically. When you modify objects through code, especially assets on disk, you must signal those changes. Whether through `SetDirty()`, `Undo.RecordObject()`, or `SerializedObject.ApplyModifiedProperties()`, marking changes ensures your work persists. Master this pattern, and you'll build reliable, professional Editor extensions that users can trust.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

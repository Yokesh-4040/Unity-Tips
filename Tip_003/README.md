# #UNITY TIPS 003/100

# Mastering ColorUsage Attribute in Unity: Control Your Color Fields Like a Pro

When working with colors in Unity, the default color picker provides full RGBA control with standard color ranges. However, not every color field needs the same level of control. Sometimes you need HDR colors for emissive materials, other times you want to disable the alpha channel entirely.

The `[ColorUsage]` attribute gives you fine-grained control over what options appear in Unity's color picker, making your inspector cleaner and preventing invalid color configurations.

---

## The Problem: One-Size-Fits-All Color Pickers

By default, Unity's color fields expose:

* Full RGBA channels (including alpha)
* Standard color range (0-1)
* No HDR support

This can lead to issues:

* Users accidentally modify alpha when it's not used
* Emissive materials can't access HDR values for bloom effects
* Unclear whether a color should support transparency
* Inconsistent color configurations across the project

---

## The Solution: ColorUsage Attribute

The `[ColorUsage]` attribute lets you customize the color picker behavior directly in your scripts. You can control two key aspects:

1. **HDR (High Dynamic Range)**: Enable colors beyond the standard 0-1 range for lighting and bloom effects
2. **Alpha Channel**: Show or hide the alpha slider when transparency isn't needed

---

## Basic Syntax

```csharp
[ColorUsage(showAlpha, hdr)]
public Color myColor;
```

**Parameters:**
* `showAlpha` (bool): Whether to show the alpha channel slider
* `hdr` (bool): Whether to enable HDR color values

---

## Practical Examples

### Example 1: Standard Color Without Alpha

```csharp
using UnityEngine;

public class ColorExamples : MonoBehaviour
{
    [ColorUsage(false, false)]
    public Color solidColor = Color.white;
}
```

**Use Case:** UI backgrounds, solid materials, tint colors where transparency isn't needed.

---

### Example 2: HDR Color for Emissive Materials

```csharp
using UnityEngine;

public class EmissiveMaterial : MonoBehaviour
{
    [ColorUsage(false, true)]
    public Color emissiveColor = Color.white;

    private Material material;

    void Start()
    {
        material = GetComponent<Renderer>().material;
        material.EnableKeyword("_EMISSION");
        material.SetColor("_EmissionColor", emissiveColor);
    }
}
```

**Use Case:** Glowing objects, neon signs, bloom effects, lighting that needs to be brighter than white.

---

### Example 3: Transparent Color with Alpha

```csharp
using UnityEngine;

public class UIFadeController : MonoBehaviour
{
    [ColorUsage(true, false)]
    public Color fadeColor = new Color(0, 0, 0, 0.5f);

    public void ApplyFade(UnityEngine.UI.Image image)
    {
        image.color = fadeColor;
    }
}
```

**Use Case:** UI overlays, fade effects, particle systems with transparency.

---

### Example 4: HDR Color with Alpha

```csharp
using UnityEngine;

public class AdvancedVFX : MonoBehaviour
{
    [ColorUsage(true, true)]
    public Color vfxColor = Color.white;

    private ParticleSystem particles;

    void Start()
    {
        particles = GetComponent<ParticleSystem>();
        var main = particles.main;
        main.startColor = vfxColor;
    }
}
```

**Use Case:** Advanced particle effects, magical auras, energy shields with transparency and bloom.

---

## Real-World Unity Use Cases

### Lighting System

```csharp
public class DynamicLight : MonoBehaviour
{
    [Header("Light Settings")]
    [ColorUsage(false, true)]
    public Color lightColor = Color.white;

    [Range(0f, 10f)]
    public float intensity = 1f;

    private Light lightComponent;

    void Start()
    {
        lightComponent = GetComponent<Light>();
        UpdateLightColor();
    }

    void UpdateLightColor()
    {
        lightComponent.color = lightColor;
    }
}
```

---

### Post-Processing Tint

```csharp
public class PostProcessTint : MonoBehaviour
{
    [Header("Color Grading")]
    [ColorUsage(false, false)]
    public Color tintColor = Color.white;

    [ColorUsage(false, true)]
    public Color bloomTint = Color.white;

    public void ApplyColorGrading()
    {
        // Apply to post-processing volume
        // tintColor for basic color grading
        // bloomTint for HDR bloom effects
    }
}
```

---

### UI Theme Manager

```csharp
public class UITheme : MonoBehaviour
{
    [Header("Solid Colors")]
    [ColorUsage(false, false)]
    public Color primaryColor = new Color(0.2f, 0.4f, 0.8f);

    [ColorUsage(false, false)]
    public Color secondaryColor = new Color(0.8f, 0.4f, 0.2f);

    [Header("Transparent Colors")]
    [ColorUsage(true, false)]
    public Color overlayColor = new Color(0, 0, 0, 0.7f);

    [ColorUsage(true, false)]
    public Color tooltipBackground = new Color(0.1f, 0.1f, 0.1f, 0.9f);
}
```

---

### Particle System Controller

```csharp
public class ParticleController : MonoBehaviour
{
    [Header("Particle Colors")]
    [ColorUsage(true, true)]
    public Color startColor = Color.white;

    [ColorUsage(true, true)]
    public Color endColor = new Color(1f, 0.5f, 0f, 0f);

    void Start()
    {
        var particles = GetComponent<ParticleSystem>();
        var main = particles.main;

        var gradient = new ParticleSystem.MinMaxGradient(startColor, endColor);
        main.startColor = gradient;
    }
}
```

---

## Comparison: Before and After

### Before (No Attribute)

```csharp
public Color emissiveGlow = Color.white; // Limited to 0-1 range
```

**Issues:**
* Can't create colors bright enough for bloom
* User might accidentally change alpha when not needed
* Not clear what the color is used for

### After (With ColorUsage)

```csharp
[ColorUsage(false, true)]
public Color emissiveGlow = Color.white * 2f; // Can exceed 1.0 for HDR
```

**Benefits:**
* Clear HDR support for bloom effects
* Alpha channel hidden when not needed
* Self-documenting code

---

## Best Practices

1. **Disable Alpha When Not Used**: If your material or shader doesn't use transparency, hide the alpha channel with `[ColorUsage(false, false)]`

2. **Enable HDR for Emissive Properties**: Any color used for emission, bloom, or lighting effects should use `[ColorUsage(false, true)]`

3. **Use Descriptive Names**: Combine ColorUsage with clear variable names
   ```csharp
   [ColorUsage(false, true)]
   public Color emissiveColor; // Clear this is for emission
   ```

4. **Group Related Colors**: Use headers to organize color properties
   ```csharp
   [Header("Base Colors")]
   [ColorUsage(false, false)]
   public Color baseColor;

   [Header("Effects")]
   [ColorUsage(false, true)]
   public Color glowColor;
   ```

5. **Set Sensible Defaults**: Initialize HDR colors with appropriate intensity
   ```csharp
   [ColorUsage(false, true)]
   public Color bloom = Color.white * 3f; // 3x intensity for visible bloom
   ```

---

## Common Patterns

### Material Property Exposure

```csharp
public class MaterialController : MonoBehaviour
{
    [SerializeField, ColorUsage(false, false)]
    private Color _baseColor = Color.white;

    [SerializeField, ColorUsage(false, true)]
    private Color _emissionColor = Color.white;

    private Material material;

    void Start()
    {
        material = GetComponent<Renderer>().material;
        UpdateMaterialColors();
    }

    void UpdateMaterialColors()
    {
        material.SetColor("_BaseColor", _baseColor);
        material.SetColor("_EmissionColor", _emissionColor);
    }
}
```

---

## Technical Details

### HDR Color Values

When HDR is enabled, colors can have RGB values greater than 1.0:

```csharp
[ColorUsage(false, true)]
public Color hdrColor = new Color(2f, 1.5f, 3f); // Valid HDR color
```

This is essential for:
* Bloom post-processing effects
* Emissive materials that need to glow
* Realistic lighting that exceeds standard brightness

### Inspector Behavior

| ColorUsage Parameters | Alpha Slider | HDR Slider | Use Case |
|----------------------|--------------|------------|----------|
| `(false, false)` | Hidden | Disabled | Solid colors, tints |
| `(true, false)` | Visible | Disabled | Transparency effects |
| `(false, true)` | Hidden | Enabled | Emissive, lighting |
| `(true, true)` | Visible | Enabled | Advanced VFX |

---

## Conclusion

The `[ColorUsage]` attribute is a simple yet powerful tool that improves both the developer experience and prevents configuration errors. By explicitly controlling alpha and HDR options, you create more intuitive inspectors and ensure colors are used correctly throughout your project.

This small attribute demonstrates Unity's philosophy: provide the right amount of control at the right time, making complex systems more manageable and less error-prone.

---

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*

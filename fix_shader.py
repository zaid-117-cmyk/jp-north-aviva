import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    content = f.read()

bt = chr(96)

shader_block = f"""const FilmGrainVignetteShader = {{
    uniforms: {{
        'tDiffuse': {{ value: null }},
        'time': {{ value: 0 }},
        'grainStrength': {{ value: 0.015 }}, // 1.5% film grain
        'vignetteStrength': {{ value: 0.18 }}, // Faint edge vignette
        'vignetteRadius': {{ value: 0.85 }}
    }},
    vertexShader: {bt}
        varying vec2 vUv;
        void main() {{
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }}
    {bt},
    fragmentShader: {bt}
        uniform sampler2D tDiffuse;
        uniform float time;
        uniform float grainStrength;
        uniform float vignetteStrength;
        uniform float vignetteRadius;
        varying vec2 vUv;

        float hashNoise(vec2 p) {{
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }}

        void main() {{
            vec4 color = texture2D(tDiffuse, vUv);
            vec2 grainCoord = vUv * vec2(1920.0, 1080.0) + vec2(time * 37.0, time * 73.0);
            float g = (hashNoise(grainCoord) - 0.5) * grainStrength;
            vec3 finalColor = color.rgb + vec3(g);

            vec2 distFromCenter = (vUv - 0.5) * vec2(1.2, 1.0);
            float len = length(distFromCenter);
            float vig = smoothstep(vignetteRadius, vignetteRadius - 0.45, len);
            finalColor = mix(finalColor * (1.0 - vignetteStrength), finalColor, vig);

            gl_FragColor = vec4(clamp(finalColor, 0.0, 1.0), color.a);
        }}
    {bt}
}};"""

# Match from "const FilmGrainVignetteShader = {" to the matching closing "};"
pattern = r'const FilmGrainVignetteShader = \{[\s\S]*?\n\};'
new_content, count = re.subn(pattern, shader_block, content)
print(f"Replaced {count} occurrences")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

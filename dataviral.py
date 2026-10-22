Run set -euo pipefail
  set -euo pipefail
  args=()
  if [[ -n "$EPISODE" ]]; then args+=(--episode "$EPISODE"); fi
  if [[ "$PUBLISH" == true ]]; then args+=(--publish); fi
  if [[ "$AUTO" == true || ( "$PUBLISH" == true && -z "$EPISODE" ) ]]; then
    args+=(--auto-publish)
  fi
  if [[ -n "$APPROVED" ]]; then args+=(--approved-id "$APPROVED"); fi
  python dataviral.py "${args[@]}"
  shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0}
  env:
    PYTHONUNBUFFERED: 1
    OPENROUTER_MODEL: openrouter/free
    GROQ_API_KEY: 
    GEMINI_API_KEY: ***
    OPENROUTER_API_KEY: ***
    INSTAGRAM_TOKEN: ***
    INSTAGRAM_USER_ID: ***
    IG_GRAPH_VERSION: v25.0
    IG_EXPECTED_USERNAME: dato_wow_
    GH_TOKEN: ***
    GITHUB_REPOSITORY: acesped/dataviral
    GITHUB_REF_NAME: main
    pythonLocation: /opt/hostedtoolcache/Python/3.11.17/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.17/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.17/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.17/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.17/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.17/x64/lib
    PUBLISH: true
    AUTO: true
    EPISODE: 
    APPROVED: 
Episodio aleatorio equilibrado: DV-249 | categoria: Tecnología y dinero | publicados de esa categoria: 5
Modelos gratuitos disponibles: google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, dots-studio/dots-3-note-preview:free, liquid/lfm-2.5-2.6b:free, minimax/minimax-m3.1-flash:free, nvidia/nemotron-3-super-120b-a12b:free, nvidia/nemotron-3.5-super-vl:free
OpenRouter etapa 1: google/gemma-4-26b-a4b-it:free: HTTP 429 (provider): modelo temporalmente saturado
OpenRouter etapa 1: google/gemma-4-31b-it:free: HTTP 429 (provider): modelo temporalmente saturado
Narración validada con dots-studio/dots-3-note-preview:free
OpenRouter etapa 2: dots-studio/dots-3-note-preview:free: Escena 1: requiere entre 3 y 9 palabras, tiene 11
OpenRouter etapa 2: google/gemma-4-26b-a4b-it:free: HTTP 429 (provider): modelo temporalmente saturado
OpenRouter etapa 2: google/gemma-4-31b-it:free: HTTP 429 (provider): modelo temporalmente saturado
OpenRouter etapa 2: liquid/lfm-2.5-2.6b:free: HTTP 504: {"error":{"message":"Provider returned error","code":504,"metadata":{"raw":"error code: 504\n","provider_name":"Liquid","is_byok":
OpenRouter etapa 2: minimax/minimax-m3.1-flash:free: respuesta truncada: el modelo consumió todos los tokens sin texto visible
OpenRouter etapa 2: nvidia/nemotron-3-super-120b-a12b:free: HTTP 404: {"error":{"message":"Provider returned error","code":404,"metadata":{"raw":"{\"status\":404,\"title\":\"Not Found\",\"detail\":\"F
OpenRouter etapa 2: nvidia/nemotron-3.5-super-vl:free: Escena 1: supera 52 caracteres; reformular, no truncar
Recuperación inicial insuficiente (solo se recuperaron 1 mensajes completos y distintos (requiere 5)); intentando completar solo mensajes faltantes
IA complemento 1: dots-studio/dots-3-note-preview:free devolvió 5 posibles frases
IA complemento 2: google/gemma-4-26b-a4b-it:free: HTTP 429 (provider): modelo temporalmente saturado
IA complemento 3: google/gemma-4-31b-it:free: HTTP 429 (provider): modelo temporalmente saturado
IA complemento 4: liquid/lfm-2.5-2.6b:free: respuesta truncada: el modelo consumió todos los tokens sin texto visible
IA complemento 5: minimax/minimax-m3.1-flash:free: respuesta truncada: el modelo consumió todos los tokens sin texto visible
IA complemento 6: nvidia/nemotron-3-super-120b-a12b:free: HTTP 404: {"error":{"message":"Provider returned error","code":404,"metadata":{"raw":"{\"status\":404,\"title\":\"Not Found\",\"de
IA complemento 7: nvidia/nemotron-3.5-super-vl:free: HTTP 502: {"error":{"message":"Provider returned error","code":502,"metadata":{"raw":"{\"message\":\"Failed to generate completion
Traceback (most recent call last):
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 920, in create_ai_episode
    visuals = _mensajes_recuperados(narration, respuestas_parciales)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 763, in _mensajes_recuperados
    raise ValueError(f'solo se recuperaron {len(valid)} mensajes completos y distintos (requiere 5)')
ValueError: solo se recuperaron 1 mensajes completos y distintos (requiere 5)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 926, in create_ai_episode
    visuals = _completar_mensajes_con_ia(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 821, in _completar_mensajes_con_ia
    return _mensajes_recuperados(narration, pool)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 763, in _mensajes_recuperados
    raise ValueError(f'solo se recuperaron {len(valid)} mensajes completos y distintos (requiere 5)')
ValueError: solo se recuperaron 2 mensajes completos y distintos (requiere 5)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 1811, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 1792, in main
    generated=create_ai_episode(ep)
              ^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/dataviral/dataviral/dataviral.py", line 933, in create_ai_episode
    raise RuntimeError(
RuntimeError: Narración válida, pero no se obtuvieron cinco mensajes seguros. OpenRouter: nvidia/nemotron-3.5-super-vl:free: Escena 1: supera 52 caracteres; reformular, no truncar. Recuperación: solo se recuperaron 2 mensajes completos y distintos (requiere 5). No se publicó nada.
Error: Process completed with exit code 1.

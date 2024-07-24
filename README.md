# Audiosity Project

vAudiosity Project is a multifaceted application designed to analyze and explore music in various creative ways.

## Top 100 US-Charts Analysis

With this app, users can delve into the top 100 US-Charts from 1959 to 2023, examining lyrics for similarities over the decades. This feature offers insights into the evolution of popular music themes and trends.

## Image Generation from Lyrics

Another exciting feature of the Audiosity Project is the ability to generate images based on song lyrics. Users can transform lyrical content into visually captivating representations, adding a new dimension to their music listening experience.

## Perfect Matching Song

Additionally, users can upload an image and receive a perfect matching song based on its content. This innovative feature combines image recognition technology with music recommendation algorithms to offer personalized music suggestions.

Audiosity Project provides a unique and immersive way to interact with music, offering both analytical insights and creative exploration opportunities.

## installation / use

To run the Audiosity WebApp from the command line, you need to simply start the Django server like this:
```
python manage.py runserver
```

The first run might take a while longer as the image generator first installs all the necessary models and dependencies first in order to run.

Please be advised that 10gb of storage and a GPU are recommended to run this app.

## Credits for the Stable Diffusion UI

based on: https://github.com/AUTOMATIC1111/stable-diffusion-webui

Licenses for borrowed code can be found in `Settings -> Licenses` screen, and also in `html/licenses.html` file.

- Stable Diffusion - https://github.com/Stability-AI/stablediffusion, https://github.com/CompVis/taming-transformers
- k-diffusion - https://github.com/crowsonkb/k-diffusion.git
- Spandrel - https://github.com/chaiNNer-org/spandrel implementing
  - GFPGAN - https://github.com/TencentARC/GFPGAN.git
  - CodeFormer - https://github.com/sczhou/CodeFormer
  - ESRGAN - https://github.com/xinntao/ESRGAN
  - SwinIR - https://github.com/JingyunLiang/SwinIR
  - Swin2SR - https://github.com/mv-lab/swin2sr
- LDSR - https://github.com/Hafiidz/latent-diffusion
- MiDaS - https://github.com/isl-org/MiDaS
- Ideas for optimizations - https://github.com/basujindal/stable-diffusion
- Cross Attention layer optimization - Doggettx - https://github.com/Doggettx/stable-diffusion, original idea for prompt editing.
- Cross Attention layer optimization - InvokeAI, lstein - https://github.com/invoke-ai/InvokeAI (originally http://github.com/lstein/stable-diffusion)
- Sub-quadratic Cross Attention layer optimization - Alex Birch (https://github.com/Birch-san/diffusers/pull/1), Amin Rezaei (https://github.com/AminRezaei0x443/memory-efficient-attention)
- Textual Inversion - Rinon Gal - https://github.com/rinongal/textual_inversion (we're not using his code, but we are using his ideas).
- Idea for SD upscale - https://github.com/jquesnelle/txt2imghd
- Noise generation for outpainting mk2 - https://github.com/parlance-zz/g-diffuser-bot
- CLIP interrogator idea and borrowing some code - https://github.com/pharmapsychotic/clip-interrogator
- Idea for Composable Diffusion - https://github.com/energy-based-model/Compositional-Visual-Generation-with-Composable-Diffusion-Models-PyTorch
- xformers - https://github.com/facebookresearch/xformers
- DeepDanbooru - interrogator for anime diffusers https://github.com/KichangKim/DeepDanbooru
- Sampling in float32 precision from a float16 UNet - marunine for the idea, Birch-san for the example Diffusers implementation (https://github.com/Birch-san/diffusers-play/tree/92feee6)
- Instruct pix2pix - Tim Brooks (star), Aleksander Holynski (star), Alexei A. Efros (no star) - https://github.com/timothybrooks/instruct-pix2pix
- Security advice - RyotaK
- UniPC sampler - Wenliang Zhao - https://github.com/wl-zhao/UniPC
- TAESD - Ollin Boer Bohan - https://github.com/madebyollin/taesd
- LyCORIS - KohakuBlueleaf
- Restart sampling - lambertae - https://github.com/Newbeeer/diffusion_restart_sampling
- Hypertile - tfernd - https://github.com/tfernd/HyperTile
- Initial Gradio script - posted on 4chan by an Anonymous user. Thank you Anonymous user.

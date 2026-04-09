import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'gerador-fotos-tema-secret-key'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    DEFAULT_DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
    MAX_UPLOAD_FILES = 5
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB total
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    THEMES = {

        # ── Profissional ──────────────────────────────────────────────────────
        'perfil_linkedin': {
            'label': 'Perfil LinkedIn',
            'keywords_en': 'LinkedIn professional profile photo, business headshot, clean background, corporate',
            'style_hint': 'clean neutral background (grey, white or light blue), soft studio lighting, sharp focus on face',
            'outfit_hint': 'formal business attire — suit and tie for men, blazer or professional blouse for women; solid neutral colors',
        },
        'foto_corporativa': {
            'label': 'Foto corporativa escritório',
            'keywords_en': 'corporate office photo, business professional, modern office environment, glass walls, city view',
            'style_hint': 'modern open-plan office or glass-walled boardroom background, polished corporate lighting',
            'outfit_hint': 'professional office attire — dark suit or blazer with trousers/skirt; smart business formal or business casual',
        },
        'orador_terno': {
            'label': 'Orador com terno e gravata',
            'keywords_en': 'keynote speaker, business speaker, podium, conference stage, suit and tie, auditorium',
            'style_hint': 'large conference stage with dramatic spotlights, presentation screens in background, powerful presenter stance',
            'outfit_hint': 'elegant dark suit with tie and dress shirt for men; formal blazer with dress for women; authoritative and polished look',
        },
        'branding_redes': {
            'label': 'Branding para redes sociais',
            'keywords_en': 'personal branding photo, social media profile, influencer portrait, vibrant studio background',
            'style_hint': 'vibrant branded background with geometric elements, bold modern color palette, studio-quality professional lighting',
            'outfit_hint': 'stylish well-coordinated outfit matching a personal brand — blazer, casual-chic, or trendy professional; bold accessories welcome',
        },
        'foto_curriculo': {
            'label': 'Foto para currículo',
            'keywords_en': 'resume CV headshot, professional portrait, plain background, formal photo',
            'style_hint': 'plain white or light grey background, front-facing headshot, neutral professional lighting, formal and approachable',
            'outfit_hint': 'formal attire — dark suit or blazer; solid neutral colors; avoid patterns or casual clothing',
        },
        'ceo_executivo': {
            'label': 'CEO / executivo em sala de reunião',
            'keywords_en': 'CEO executive portrait, boardroom, conference room, leadership, power, city skyline',
            'style_hint': 'elegant boardroom or executive office with city skyline view, sophisticated lighting, powerful confident pose',
            'outfit_hint': 'premium dark suit with tie or luxury business attire; powerful and authoritative executive presence',
        },
        'medico_jaleco': {
            'label': 'Médico com jaleco',
            'keywords_en': 'doctor white coat, medical professional, hospital clinic, stethoscope, modern healthcare',
            'style_hint': 'modern hospital or clinic background, clean white medical environment, professional medical lighting',
            'outfit_hint': 'white doctor coat (jaleco) worn over professional clothing, with stethoscope around the neck',
        },
        'advogado_toga': {
            'label': 'Advogado com toga',
            'keywords_en': 'lawyer in robe, law office, bookshelves, legal professional, justice, courtroom',
            'style_hint': 'law office with floor-to-ceiling bookshelves of legal volumes, or formal courtroom, prestigious and authoritative',
            'outfit_hint': "lawyer's black robe (toga) with white jabots/collar; or formal dark suit with tie in a law office setting",
        },
        'coach_palestrante': {
            'label': 'Coach / palestrante no palco',
            'keywords_en': 'motivational speaker, life coach, stage, auditorium, crowd, microphone, energy',
            'style_hint': 'large auditorium stage with spotlights, enthusiastic audience silhouettes, energetic and inspiring atmosphere',
            'outfit_hint': 'smart business casual — fitted blazer with open-collar shirt; charismatic and approachable yet professional look',
        },
        'cartao_visita': {
            'label': 'Foto para cartão de visita',
            'keywords_en': 'business card headshot, professional portrait, clean polished look, warm lighting',
            'style_hint': 'clean slightly blurred or solid background, half-body portrait, warm and confident professional lighting',
            'outfit_hint': 'professional attire matching the industry — suit for corporate, smart casual for creative fields; neat and polished',
        },

        # ── Datas comemorativas ───────────────────────────────────────────────
        'dia_das_maes': {
            'label': 'Ensaio Dia das Mães',
            'keywords_en': "Mother's Day photoshoot, flowers, roses, peonies, floral garden, pastel celebration, maternal love",
            'style_hint': 'soft pastel colors, lush floral background with roses and peonies, warm golden-hour lighting, tender loving atmosphere',
            'outfit_hint': 'elegant floral dress or feminine blouse in soft pink, lavender or cream tones; delicate jewelry and accessories',
        },
        'pascoa': {
            'label': 'Ensaio Páscoa',
            'keywords_en': 'Easter photoshoot, colorful eggs, Easter bunny, spring flowers, pastel colors, chocolate basket',
            'style_hint': 'bright spring garden setting, pastel-colored eggs and flowers, cheerful and fresh atmosphere, soft natural light',
            'outfit_hint': 'light spring outfit — pastel-colored dress, floral print, or bright casual clothing; bunny ears headband optional',
        },
        'natal': {
            'label': 'Ensaio Natal',
            'keywords_en': 'Christmas photoshoot, snow, decorated Christmas tree, ornaments, Santa Claus, festive lights, gift boxes',
            'style_hint': 'warm festive indoor setting with glowing Christmas tree, red and green decorations, cozy fireplace atmosphere',
            'outfit_hint': 'Christmas outfit — red or green sweater, Santa hat, cozy holiday knit, or elegant festive dress; warm and festive',
        },
        'dia_dos_pais': {
            'label': 'Ensaio Dia dos Pais',
            'keywords_en': "Father's Day, outdoors, adventure, strength, nature, barbecue, tools, workshop",
            'style_hint': 'warm outdoor setting — backyard with barbecue, green park, or garage; bold warm colors, relaxed masculine atmosphere',
            'outfit_hint': 'casual but neat masculine outfit — polo shirt, jeans or chinos, or casual button-down shirt; relaxed and confident',
        },
        'dia_dos_namorados': {
            'label': 'Ensaio Dia dos Namorados',
            'keywords_en': "Valentine's Day, romantic, red roses, hearts, candlelight, love, couple, dinner",
            'style_hint': 'romantic candlelit restaurant or rose-filled room, red and pink tones, soft warm bokeh lights, elegant romantic atmosphere',
            'outfit_hint': 'elegant romantic attire — red or pink dress for women, dark suit or dress shirt for men; sophisticated and romantic',
        },
        'festa_junina': {
            'label': 'Festa Junina / Julina',
            'keywords_en': 'Brazilian June festival, colorful flags, straw hat, checkered outfit, forró dance, corn, countryside party',
            'style_hint': 'vibrant Brazilian June festival with colorful bunting flags, rustic wooden structures, warm festive countryside atmosphere',
            'outfit_hint': 'traditional festa junina outfit — colorful checkered or floral dress with pigtails for women; checkered shirt, straw hat, and suspenders for men',
        },
        'reveillon': {
            'label': 'Réveillon / Ano Novo',
            'keywords_en': 'New Year Eve, fireworks, celebration, confetti, champagne, midnight countdown, glitter, party',
            'style_hint': 'glamorous New Year party or beachfront fireworks scene, golden and silver tones, glittering confetti, festive night sky',
            'outfit_hint': 'glamorous New Year outfit — sparkly or sequined dress/suit, white clothing (Brazilian tradition), or elegant formal party wear',
        },
        'halloween': {
            'label': 'Halloween',
            'keywords_en': 'Halloween, carved pumpkins, spooky night, costumes, haunted house, bats, full moon, fog',
            'style_hint': 'dark spooky Halloween setting with jack-o-lanterns and haunted house, orange and black atmosphere, mysterious and fun',
            'outfit_hint': 'Halloween costume — witch, vampire, skeleton, zombie, or any creative spooky costume matching the chosen character',
        },

        # ── Ensaios especiais ─────────────────────────────────────────────────
        'ensaio_gestante': {
            'label': 'Ensaio gestante',
            'keywords_en': 'maternity photoshoot, pregnant woman, beautiful pregnancy, flowers, soft light, expecting mother, baby bump',
            'style_hint': 'soft ethereal lighting with floral or garden setting, pastel tones, elegant and emotional atmosphere celebrating motherhood',
            'outfit_hint': 'elegant maternity dress — flowing gown in white, cream or pastel; form-fitting dress that beautifully showcases the baby bump',
        },
        'ensaio_newborn': {
            'label': 'Ensaio newborn',
            'keywords_en': 'newborn baby, family portrait, tender moment, nursery, soft blankets, new life, delicate',
            'style_hint': 'soft warm nursery with gentle natural light, cream and pastel tones, tender and precious family moment',
            'outfit_hint': 'soft comfortable outfit in neutral tones — cream, beige or light grey; casual and cozy, warm and loving feel',
        },
        'aniversario_crianca': {
            'label': 'Aniversário de criança',
            'keywords_en': 'child birthday party, colorful balloons, birthday cake, confetti, celebration, joy, kids party decorations',
            'style_hint': 'vibrant colorful birthday party with balloons, streamers and birthday cake, joyful and festive atmosphere',
            'outfit_hint': 'festive birthday outfit — colorful party dress, birthday crown or tiara, or themed costume; fun and celebratory look',
        },
        'familia_campo': {
            'label': 'Ensaio família no campo',
            'keywords_en': 'family countryside photoshoot, green meadow, nature, golden hour, rural landscape, wildflowers',
            'style_hint': 'lush green countryside with golden hour lighting, natural wooden fences or wildflower fields, warm wholesome family atmosphere',
            'outfit_hint': 'coordinated casual family outfits — earth tones, beige, white and denim; comfortable and natural-looking for outdoor setting',
        },
        'casal_romantico': {
            'label': 'Ensaio casal romântico',
            'keywords_en': 'romantic couple photoshoot, love, embrace, sunset, rose garden, tender moment, golden light',
            'style_hint': 'romantic outdoor setting with golden sunset or blooming garden, warm golden tones, soft bokeh background, intimate atmosphere',
            'outfit_hint': 'coordinated couple outfits in complementary colors — elegant casual (dress and blazer) or formal romantic attire for studio',
        },
        'casamento': {
            'label': 'Foto de casamento',
            'keywords_en': 'wedding photo, bride and groom, white dress, ceremony, flowers, elegant venue, celebration',
            'style_hint': 'elegant wedding venue with floral decorations, white and gold tones, magical romantic lighting, timeless atmosphere',
            'outfit_hint': 'wedding attire — elegant white or ivory wedding dress for bride; dark formal suit or tuxedo for groom; wedding accessories included',
        },
        'formatura': {
            'label': 'Formatura com beca',
            'keywords_en': 'graduation, academic gown, cap, diploma, university ceremony, achievement, celebration, campus',
            'style_hint': 'prestigious university campus or elegant graduation ceremony hall, traditional academic atmosphere, proud and celebratory moment',
            'outfit_hint': 'graduation gown (beca) with academic cap (birra) over formal professional attire; holding diploma or scroll',
        },
        'debutante': {
            'label': '15 anos / debutante',
            'keywords_en': 'quinceañera, sweet fifteen birthday, princess ball gown, tiara, roses, elegant ballroom, fairy tale',
            'style_hint': 'magical ballroom or elegant garden with rose petals and fairy lights, pink and gold palette, princess fairytale atmosphere',
            'outfit_hint': 'elegant ball gown in pink, lilac or soft gold with tiara/crown; elbow-length gloves optional; classic debutante princess look',
        },

        # ── Cenários do mundo ─────────────────────────────────────────────────
        'muralha_china': {
            'label': 'Muralha da China',
            'keywords_en': 'Great Wall of China, Chinese mountains, ancient architecture, tourism, majestic landscape, misty',
            'style_hint': 'dramatic panoramic view of the Great Wall winding through lush mountain ranges, misty atmospheric depth, ancient grandeur',
            'outfit_hint': 'smart casual tourist attire — comfortable stylish clothing for sightseeing; optionally a traditional Chinese-inspired outfit',
        },
        'torre_eiffel': {
            'label': 'Torre Eiffel — Paris',
            'keywords_en': 'Eiffel Tower, Paris, France, romantic city, Seine river, Parisian street, European landmark',
            'style_hint': 'iconic Eiffel Tower with Parisian boulevard or riverbank, warm golden hour light, romantic European atmosphere',
            'outfit_hint': 'chic Parisian style — striped shirt, beret, trench coat, or elegant dress; classic French fashion aesthetic',
        },
        'times_square': {
            'label': 'Times Square — Nova York',
            'keywords_en': 'Times Square, New York City, bright neon lights, Broadway, urban energy, yellow cabs, iconic',
            'style_hint': 'vibrant Times Square at night with glowing neon billboards and yellow cabs, dynamic urban energy, iconic NYC atmosphere',
            'outfit_hint': 'trendy urban fashion — stylish streetwear, jeans with leather jacket, or chic city outfit; New York street style energy',
        },
        'praia_tropical': {
            'label': 'Praia paradisíaca tropical',
            'keywords_en': 'tropical paradise beach, turquoise ocean, white sand, palm trees, crystal clear water, summer',
            'style_hint': 'stunning tropical beach with turquoise water and white sand, lush palm trees, vibrant tropical colors, paradise vacation',
            'outfit_hint': 'beach vacation outfit — swimwear, colorful cover-up, sundress, or resort-style fashion; light and breezy tropical clothing',
        },
        'montanhas_nevadas': {
            'label': 'Montanhas nevadas',
            'keywords_en': 'snowy mountains, winter Alps, ski resort, frozen peaks, winter wonderland, pine forest',
            'style_hint': 'majestic snow-covered mountain peaks, crisp winter atmosphere, pine forest and ski slopes, stunning alpine panorama',
            'outfit_hint': 'warm winter mountain outfit — ski jacket, snow pants, beanie, gloves and boots; stylish and functional alpine wear',
        },
        'coliseu_roma': {
            'label': 'Coliseu — Roma',
            'keywords_en': 'Colosseum Rome, Italy, ancient Roman architecture, historical landmark, gladiator arena, golden hour',
            'style_hint': 'magnificent Colosseum at golden hour or sunset, warm terracotta and amber tones, ancient Roman grandeur',
            'outfit_hint': 'smart casual tourist or elegant travel outfit; alternatively, Roman-inspired toga or gladiator costume for creative look',
        },
        'disney': {
            'label': 'Disney / parque temático',
            'keywords_en': 'Disney theme park, Cinderella castle, magical, colorful, fairy tale, Disney characters, fireworks',
            'style_hint': 'magical Disney castle with fireworks and fairy dust, vibrant colorful theme park atmosphere, pure joy and wonder',
            'outfit_hint': 'Disney-themed outfit — dress inspired by a Disney princess, Mickey Mouse ears headband, or fun theme park casual attire',
        },
        'safari_africano': {
            'label': 'Safari africano',
            'keywords_en': 'African safari, savanna, wildlife, lions, elephants, jeep, golden grasslands, sunset adventure',
            'style_hint': 'vast golden African savanna at sunset with wildlife silhouettes, warm amber and orange tones, adventurous wild atmosphere',
            'outfit_hint': 'classic safari outfit — khaki pants, beige safari shirt, wide-brim hat, leather boots; classic explorer adventurer look',
        },

        # ── Esportes ──────────────────────────────────────────────────────────
        'ringue_ufc': {
            'label': 'Ringue de UFC / MMA',
            'keywords_en': 'UFC octagon ring, MMA fighter, combat sports, arena, championship belt, crowd, intense',
            'style_hint': 'dramatic UFC octagon with bright arena lights and crowd in background, intense powerful fighting atmosphere',
            'outfit_hint': 'MMA fighter gear — shorts/trunks, fingerless gloves, optional title belt; athletic and fierce fighter appearance',
        },
        'campo_futebol': {
            'label': 'Campo de futebol — jogador',
            'keywords_en': 'soccer football player, professional stadium, green pitch, crowd roaring, footballer, goal',
            'style_hint': 'professional football stadium with roaring crowd in stands, vibrant green pitch under floodlights, sports atmosphere',
            'outfit_hint': 'football/soccer kit — jersey, shorts, shin guards and cleats; classic professional footballer uniform with team colors',
        },
        'quadra_nba': {
            'label': 'Quadra de basquete NBA',
            'keywords_en': 'NBA basketball court, professional player, arena, slam dunk, hardwood floor, packed crowd',
            'style_hint': 'professional NBA arena with gleaming hardwood floor and packed crowd, dramatic arena lighting, electrifying atmosphere',
            'outfit_hint': 'NBA basketball uniform — jersey, shorts and basketball shoes; classic professional basketball player look',
        },
        'formula1': {
            'label': 'Corrida de Fórmula 1',
            'keywords_en': 'Formula 1 race car, F1 driver, pit lane, circuit, speed, racing suit, helmet, podium',
            'style_hint': 'F1 pit lane or racing circuit with sleek race cars, dynamic speed energy, high-octane motorsport atmosphere',
            'outfit_hint': 'F1 racing driver suit (fireproof overalls) with helmet under arm and racing gloves; branded team racing outfit',
        },

        # ── Criativos ─────────────────────────────────────────────────────────
        'capa_revista': {
            'label': 'Capa de revista',
            'keywords_en': 'magazine cover, celebrity portrait, glamour, editorial fashion, high-end photoshoot, bold',
            'style_hint': 'magazine-cover composition with bold typography space, high-fashion editorial lighting, glamorous and polished studio',
            'outfit_hint': 'high-fashion editorial outfit — glamorous evening wear, designer clothing, or bold fashion statement pieces; full cover glamour',
        },
        'tapete_vermelho': {
            'label': 'Tapete vermelho — Hollywood',
            'keywords_en': 'red carpet Hollywood, celebrity premiere, glamour, paparazzi cameras, luxury fashion, awards ceremony',
            'style_hint': 'glamorous Hollywood red carpet with flashing cameras and luxury venue entrance, celebrity premiere atmosphere',
            'outfit_hint': 'black-tie red carpet attire — glamorous evening gown or tuxedo; luxurious designer fashion with jewelry and accessories',
        },
        'astronauta': {
            'label': 'Astronauta no espaço',
            'keywords_en': 'astronaut, outer space, Earth from orbit, NASA spacesuit, stars, galaxy, space station, cosmos',
            'style_hint': 'breathtaking outer space with Earth visible below, stunning galaxy and stars, dramatic zero-gravity atmosphere',
            'outfit_hint': 'full NASA-style white spacesuit with helmet; classic astronaut gear floating in space or aboard a spacecraft',
        },
        'super_heroi': {
            'label': 'Super-herói personalizado',
            'keywords_en': 'superhero, cape, cityscape, powers, hero pose, comic book, dynamic action, original character',
            'style_hint': 'dramatic cityscape or stormy sky background with heroic lighting, dynamic action-hero composition, cinematic superhero feel',
            'outfit_hint': 'custom superhero costume — fitted suit with cape, mask optional, heroic emblem on chest; original design inspired by the person',
        },
        'ensaio_fitness': {
            'label': 'Ensaio fitness / academia',
            'keywords_en': 'fitness photoshoot, gym, athletic, workout, sports performance, weights, dumbbells, strength',
            'style_hint': 'modern gym with weights and equipment, dramatic fitness photography lighting, athletic and energetic atmosphere',
            'outfit_hint': 'athletic fitness wear — compression shorts or leggings, fitted sports top or tank top, athletic shoes; form-fitting sportswear',
        },
        'estilo_barbie': {
            'label': 'Estilo Barbie / boneca',
            'keywords_en': 'Barbie doll aesthetic, pink world, glamour, fashion doll, pink dream house, plastic fantastic',
            'style_hint': 'iconic pink Barbie world with dream house and sparkling accessories, saturated pink palette, glossy doll-like aesthetic',
            'outfit_hint': 'iconic Barbie-style outfit — bright hot pink dress, jumpsuit or glamorous ensemble; bold pink is essential; doll-like fashion',
        },
        'foto_pet': {
            'label': 'Foto de pet / animal de estimação',
            'keywords_en': 'pet photo, dog, cat, owner with pet, animal companion, adorable lifestyle, bond',
            'style_hint': 'warm cozy home setting or beautiful park, soft natural lighting, heartwarming bond between owner and beloved pet',
            'outfit_hint': 'casual comfortable outfit — jeans, sweater or casual shirt; relaxed clothing perfect for a natural pet photoshoot',
        },
        'aquarela': {
            'label': 'Ensaio aquarela / pintura artística',
            'keywords_en': 'watercolor portrait, artistic painting, colorful paint splashes, art aesthetic, painterly photograph',
            'style_hint': 'beautiful blend of photography and watercolor painting with colorful artistic splashes and soft painterly textures',
            'outfit_hint': 'elegant or creative outfit in soft complementary colors — flowy dress, or artistic bohemian style; visually interesting clothing',
        },
        'floresta_encantada': {
            'label': 'Fundo de floresta encantada',
            'keywords_en': 'enchanted forest, magical woods, fairy lights, fantasy, ethereal, mystical glowing nature',
            'style_hint': 'magical glowing forest with fairy lights and bioluminescent plants, ethereal mist and magical bokeh, fairytale atmosphere',
            'outfit_hint': 'magical fantasy outfit — flowing ethereal dress, fairy or woodland creature costume, floral crown; enchanted fairy aesthetic',
        },
        'anime': {
            'label': 'Estilo anime / personagem',
            'keywords_en': 'anime style character, Japanese animation aesthetic, manga art, colorful anime scene, animated portrait',
            'style_hint': 'vibrant anime-style artistic rendering with detailed anime background and characteristic anime art style, manga-inspired aesthetic',
            'outfit_hint': 'anime-inspired outfit — school uniform, warrior costume, maid dress, or iconic anime character clothing; bold and faithful to anime style',
        },
        'ensaio_inverno': {
            'label': 'Ensaio inverno / neve',
            'keywords_en': 'winter photoshoot, snow, frozen landscape, snowflakes, cozy winter, snow-covered trees',
            'style_hint': 'serene snowy winter landscape with snow-covered trees and delicate snowflakes, cool blue-white tones, magical winter wonderland',
            'outfit_hint': 'cozy winter fashion — long wool coat, warm scarf, gloves and boots; elegant winter ensemble in whites, greys or deep jewel tones',
        },
        'perfil_artistico': {
            'label': 'Foto de perfil artística (AI art)',
            'keywords_en': 'artistic AI portrait, digital art, creative profile photo, surreal, beautiful, stylized, dramatic',
            'style_hint': 'stunning AI-art portrait with dramatic artistic lighting, creative color grading, painterly and highly stylized photographic aesthetic',
            'outfit_hint': 'dramatic and visually striking outfit — elegant dark clothing, flowing fabrics, or bold colors; strong visual impact for artistic portrait',
        },
    }

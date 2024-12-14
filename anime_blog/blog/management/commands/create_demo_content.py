import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from blog.models import Post, Category

class Command(BaseCommand):
    """
    Comando para criar posts de demonstração no banco de dados com base
    no conteúdo fornecido. Cria um usuário autor (caso não exista), categorias
    e diversos posts categorizados, cada um com uma imagem associada.
    """

    help = 'Cria posts de demonstração com base no conteúdo fornecido.'

    def handle(self, *args, **options):
        # Cria um usuário autor, caso não exista
        author, created = User.objects.get_or_create(username='admin')
        if created:
            author.set_password('admin')
            author.is_superuser = True
            author.is_staff = True
            author.save()

        # Criar categorias
        cat_best, _ = Category.objects.get_or_create(name='Melhores de Sempre', description='Top Animes Clássicos')
        cat_worst, _ = Category.objects.get_or_create(name='Piores de Sempre', description='Piores Animes')
        cat_thisyear_best, _ = Category.objects.get_or_create(name='Melhores do Ano', description='Top Animes do Ano')
        cat_thisyear_worst, _ = Category.objects.get_or_create(name='Piores do Ano', description='Piores Animes do Ano')
        cat_future, _ = Category.objects.get_or_create(name='Lançamentos Futuros', description='Animes que vão estrear')
        cat_movies, _ = Category.objects.get_or_create(name='Melhores Filmes', description='Filmes imperdíveis')
        cat_winners, _ = Category.objects.get_or_create(name='Vencedores Anuais', description='Animes premiados')
        
        cats = {}
        for name, desc in categories_data.items():
            c, _ = Category.objects.get_or_create(name=name, description=desc)
            cats[name] = c

        media_path = os.path.join(settings.MEDIA_ROOT, 'posts')

        def create_post(title, content, category, image_name):
            """
            Cria um objeto Post no banco de dados, associando-o a uma imagem.
            Se a imagem especificada não existir, usa 'placeholder.jpg'.

            :param title: Título do post
            :param content: Conteúdo (texto) do post
            :param category: Objeto Category ao qual o post pertence
            :param image_name: Nome do arquivo de imagem
            """
            image_path = os.path.join(media_path, image_name)
            if not os.path.exists(image_path):
                # Se não achar a imagem, usa placeholder
                placeholder = 'placeholder.jpg'
                image_path = os.path.join(media_path, placeholder)
                if not os.path.exists(image_path):
                    # Se não tiver placeholder, erro
                    self.stdout.write(self.style.ERROR(f'Imagem placeholder não encontrada.'))
                    return
                self.stdout.write(self.style.WARNING(f'Imagem "{image_name}" não encontrada, usando "{placeholder}".'))
            with open(image_path, 'rb') as img_file:
                post = Post(
                    title=title,
                    content=content,
                    author=author,
                    category=category
                )
                post.cover_image.save(image_name, img_file, save=True)
            return post

        # Melhores de Sempre (Top 5) - descrições mais longas (mínimo 6 linhas)
        best_ever = [
            (
                "Fullmetal Alchemist: Brotherhood",
                """Fullmetal Alchemist: Brotherhood é muitas vezes considerado o pináculo do shounen. 
A história segue os irmãos Elric em uma jornada profunda de redenção após uma tentativa 
fracassada de transmutação humana. Além da aventura intensa, o anime aborda moralidade, 
sacrifício e a busca pelo significado da vida. Cada personagem é tridimensional, e 
o equilíbrio entre drama, humor e ação é impecável. Recomendo pela sua narrativa envolvente, 
mensagem inspiradora e qualidade técnica notável, que se mantêm do início ao fim.""",
                "fullmetal.jpg"
            ),
            (
                "Neon Genesis Evangelion",
                """Neon Genesis Evangelion revolucionou o gênero mecha ao mergulhar na psique de seus personagens.
A série não é apenas sobre robôs gigantes, mas sobre solidão, medo do abandono e busca por 
aceitação. Os simbolismos religiosos e filosóficos permeiam cada episódio, criando múltiplas 
camadas de interpretação. A sensação de claustrofobia emocional e as tensões entre os pilotos 
e a organização NERV marcam a experiência. Recomendo este anime pela ousadia narrativa, 
influência cultural e pela reflexão que provoca sobre a condição humana.""",
                "evangelion.jpg"
            ),
            (
                "Monster",
                """Monster é um suspense psicológico singular, focado na perseguição entre o Dr. Tenma e o 
enigmático Johan. Ao invés de magia ou poderes especiais, a história se ancora no realismo 
e na complexidade moral. Cada personagem secundário é cuidadosamente construído, 
adicionando profundidade ao mundo e aos dilemas enfrentados. A trama questiona o valor 
da vida, o peso da responsabilidade e o que nos torna humanos. A narrativa lenta e densa 
recompensa o espectador com uma experiência intensa e inesquecível.""",
                "monster.jpg"
            ),
            (
                "Gintama",
                """Gintama é a mistura perfeita de comédia, sátira e ação. Ambientada em um Japão feudal 
dominado por alienígenas, a série brinca com convenções do gênero, quebra a quarta parede 
e faz referências à cultura pop. Mas não se engane: por trás do humor nonsense, há arcos 
dramáticos e emocionantes que exploram a lealdade, a amizade e a redenção. Os personagens 
são carismáticos e evoluem no decorrer da história. Gintama surpreende por ser um anime 
extremamente versátil, capaz de fazer rir às lágrimas e chorar de emoção.""",
                "gintama.jpg"
            ),
            (
                "Death Note",
                """Death Note é um duelo intelectual entre dois gênios: Light Yagami, que encontra um caderno 
capaz de matar qualquer pessoa cujo nome seja escrito nele, e L, o detetive excêntrico que 
tenta detê-lo. O anime nos faz questionar o que é justiça e até onde podemos ir para criá-la. 
A tensão constante, a atmosfera sombria e a estratégia minuciosa dos personagens tornam cada 
episódio hipnótico. O embate moral entre poder absoluto e responsabilidade é o grande trunfo. 
Recomendo pela intensidade e pela reflexão que gera sobre ética e humanidade.""",
                "deathnote.jpg"
            ),
        ]

        for title, desc, img in best_ever:
            create_post(title, desc, cat_best, img)

        # Piores de Sempre (Top 5) - mantém descrições curtas (pode estender se quiser)
        worst_ever = [
            ("Mars of Destruction",
             "Produção amadora, roteiro confuso. Praticamente nada de valor.",
             "mars.jpg"),
            ("Skelter+Heaven",
             "Mesmo problema de Mars of Destruction: animação fraca, sem sentido.",
             "skelter.jpg"),
            ("Pupa",
             "Premissa interessante, execução péssima. Episódios curtos e censura excessiva.",
             "pupa.jpg"),
            ("Eiken",
             "Excesso de fanservice sem graça, sem história envolvente. Constrangedor.",
             "eiken.jpg"),
            ("Vampire Holmes",
             "Promessa de mistério e vampiros, entrega tédio e confusão.",
             "holmes.jpg")
        ]

        for title, desc, img in worst_ever:
            create_post(title, desc, cat_worst, img)

        # Melhores deste ano (Top 5)
        best_this_year = [
            ("Jujutsu Kaisen Season 3",
             "Continuação sólida, batalhas insanas e profundidade de personagens.",
             "jujutsu.jpg"),
            ("Solo Leveling",
             "Adaptação do webtoon. Escalada de poder do protagonista é viciante.",
             "sololeveling.jpg"),
            ("Chainsaw Man Season 2",
             "Insano, original, brutal e cativante. Expande o universo esquisito.",
             "chainsaw2.jpg"),
            ("Vinland Saga Season 3",
             "Dilemas sobre paz e redenção. Mais maduro a cada temporada.",
             "vinland3.jpg"),
            ("Spy x Family Season 2",
             "Humor, ação e ternura da família falsa mais amada do anime.",
             "spyxfamily2.jpg")
        ]

        for title, desc, img in best_this_year:
            create_post(title, desc, cat_thisyear_best, img)

        # Piores deste ano (Top 5)
        worst_this_year = [
            ("Zombie Idol Fever",
             "Tentativa de idols zumbis sem sentido. Animação pobre.",
             "zombieidol.jpg"),
            ("Love in the Outer Dimensions",
             "Romance espacial tedioso, diálogos forçados.",
             "loveouter.jpg"),
            ("Samurai Dentist",
             "Premissa engraçada, execução falha. Humor repetitivo.",
             "samuraidentist.jpg"),
            ("Kitten Warriors",
             "Gatos guerreiros mal animados. Poderia ser infantil fofo, mas falha.",
             "kitten.jpg"),
            ("Cyber Fairyland",
             "Cyberpunk e fadas sem coesão. Prometeu inovação, entregou tédio.",
             "cyberfairyland.jpg")
        ]

        for title, desc, img in worst_this_year:
            create_post(title, desc, cat_thisyear_worst, img)

        # Lançamentos Futuros (10 animes)
        future_releases = [
            ("Attack on Titan: A New Era", "Nova saga após o fim da original. Expectativa de tensão contínua.", "aot_newera.jpg"),
            ("Demon Slayer: Pillar Chronicles", "Histórias dos Hashira antes da trama principal. Profundidade dos personagens.", "ds_pillar.jpg"),
            ("My Hero Academia: Final Arc", "Arco final de Deku. Espera-se um encerramento épico.", "mha_final.jpg"),
            ("One Punch Man Season 3", "Batalhas insanas e mais desenvolvimento de personagens.", "opm_s3.jpg"),
            ("Haikyuu!! Next Generation", "Novos jogadores de vôlei, mantendo o espírito da série.", "haikyuu_next.jpg"),
            ("Mushoku Tensei Season 3", "Isekai de qualidade, evolução de Rudeus e mundo mágico.", "mushoku3.jpg"),
            ("Tokyo Revengers: The Final Time Leap", "Conclusão coerente da saga temporal. Fechar pontas soltas.", "tokyorev_final.jpg"),
            ("Chainsaw Man Season 3", "Expansão do universo insano do mangá. Expectativa alta.", "chainsaw3.jpg"),
            ("Jujutsu Kaisen: Ancients", "Explora feiticeiros do passado. Expande a lore.", "jjk_ancients.jpg"),
            ("Sword Art Online: New Frontier", "Nova era de VRMMO. Tomara que traga frescor à série.", "sao_newfrontier.jpg")
        ]

        for title, desc, img in future_releases:
            create_post(title, desc, cat_future, img)

        # Melhores Filmes
        movies = [
            ("Your Name", "História de amor no tempo e espaço, animação impecável.", "yourname.jpg"),
            ("A Viagem de Chihiro", "Obra-prima Ghibli, mundo mágico e rico em metáforas.", "chihiro.jpg"),
            ("A Voz do Silêncio", "Bullying, redenção, aceitação. Emocionalmente forte.", "vozsilencio.jpg"),
            ("Your Lie in April: The Movie", "Adaptação fiel do drama musical. Soco emocional.", "yourlie.jpg"),
            ("Made in Abyss: Dawn of the Deep Soul", "Jornada sombria, visual incrível, choca e encanta.", "madeinabyss.jpg")
        ]

        for title, desc, img in movies:
            create_post(title, desc, cat_movies, img)

        # Vencedores Anuais
        winners = [
            ("Jujutsu Kaisen (2020)", "Estreia impactante, ação fluida e carisma.", "jujutsu2020.jpg"),
            ("Attack on Titan: The Final Season Part 1 (2021)", "Tensão política, qualidade técnica.", "aot2021.jpg"),
            ("Cyberpunk: Edgerunners (2022)", "Estiloso, emocionante, inspirado no jogo.", "edgerunners2022.jpg"),
            ("Oshi no Ko (2023)", "Drama, mistério e crítica à indústria do entretenimento.", "oshinoko2023.jpg"),
            ("Solo Leveling (2024)", "Adaptação aguardada, atendeu ao hype.", "sololeveling2024.jpg")
        ]

        for title, desc, img in winners:
            create_post(title, desc, cat_winners, img)

        self.stdout.write(self.style.SUCCESS('Conteúdo de demonstração criado com sucesso!'))

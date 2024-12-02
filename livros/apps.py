from django.apps import AppConfig


class LivrosConfig(AppConfig):
    """
    Configuração da aplicação 'livros' no Django.

    Esta classe define as configurações para a aplicação 'livros', que pode incluir definições de comportamento
    padrão, configurações de banco de dados e outras opções específicas para o app. O Django usa a classe `AppConfig`
    para configurar as aplicações registradas no projeto.

    **Parâmetros:**
    - `default_auto_field`: Define o tipo de campo usado para chaves primárias automáticas. Aqui, é definido como `BigAutoField`.
    - `name`: O nome da aplicação, que neste caso é 'livros'.

    **Funcionamento:**
    - O Django automaticamente configura a aplicação 'livros' durante a inicialização do projeto.
    - A configuração `default_auto_field` especifica que o campo de chave primária para modelos deve ser um `BigAutoField`.
    - O `name` é o identificador único da aplicação no projeto.

    :param request: Objeto de configuração que é usado pelo Django para configurar a aplicação.
    :return: None
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livros'

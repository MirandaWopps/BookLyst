from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuração da aplicação 'accounts' no Django.

    Esta classe define as configurações para a aplicação 'accounts', responsável pelo gerenciamento de contas de usuário,
    incluindo o processo de autenticação, registro e gerenciamento de permissões de usuários.

    **Parâmetros:**
    - `default_auto_field`: Define o tipo de campo usado para chaves primárias automáticas. Aqui, é definido como `BigAutoField`.
    - `name`: O nome da aplicação, que neste caso é 'accounts'.

    **Funcionamento:**
    - O Django configura automaticamente a aplicação 'accounts' durante a inicialização do projeto.
    - A configuração `default_auto_field` especifica que os modelos da aplicação usarão um campo `BigAutoField` como chave primária por padrão.
    - O `name` especifica o nome da aplicação dentro do projeto.

    :param request: Objeto de configuração utilizado pelo Django para configurar a aplicação.
    :return: None
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

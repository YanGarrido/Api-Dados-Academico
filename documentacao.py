api_description = """
Esta API foi desenvolvida para centralizar e facilitar o acesso a dados acadêmicos. Ela oferece um conjunto robusto de endpoints para consulta de informações detalhadas sobre a estrutura educacional da instituição.

Utilize esta API para integrar dados acadêmicos em suas aplicações de forma simples e eficiente, garantindo consistência e acesso rápido à informação.
"""

tags_metadata = [
    {
        "name": "Students",
        "description": """
Endpoints para consultar informações sobre os alunos.

Permite a busca por listas de alunos **ativos**, **inativos** e **ex-alunos**, além de dados detalhados de um aluno específico, incluindo os cursos em que está matriculado.
        """,
    },
    {
        "name": "Professors",
        "description": """
Endpoints dedicados à consulta de informações sobre os professores.

É possível obter listas de professores **ativos** e **inativos**, bem como buscar os detalhes de um professor específico e ver todas as **disciplinas que ele leciona**.
        """,
    },
    {
        "name": "Courses",
        "description": """
Endpoints para obter informações sobre os cursos oferecidos.

Fornece a listagem de todos os cursos, detalhes de um curso específico com a **lista completa de suas disciplinas**, e funcionalidades para verificar a existência e a quantidade de alunos em **turmas ativas** por período.
        """,
    },
    {
        "name": "Subjects",
        "description": """
Endpoints para consulta de informações sobre as disciplinas.

Permite listar todas as disciplinas, buscar detalhes de uma disciplina específica (incluindo os **cursos que a oferecem**) e filtrar disciplinas de um **semestre letivo corrente**.
        """,
    },
    {
        "name": "Curriculum",
        "description": """
Endpoints para acessar as grades curriculares dos cursos.

Você pode consultar a grade **atual** de um curso específico, a grade **antiga**, ou uma visão geral das grades disponíveis.
        """,
    },
    {
        "name": "Schedules",
        "description": "Endpoint para consultar a lista de todos os **horários** de aula disponíveis na instituição.",
    },
]
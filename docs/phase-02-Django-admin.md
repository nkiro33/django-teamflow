# Phase 2 — Django Admin Setup

This phase adds Django admin configuration for the project models.

The goal is to make the data easier to inspect and manage while learning how the models relate to each other.

Django admin is not the final interface of the application. It is mainly a developer and internal management tool.

## What Is Django Admin?

Django admin is a built-in interface that Django provides for managing database records.

After models are registered in the admin, you can use the browser to:

- view records
- create records
- update records
- delete records
- search records
- filter records
- manage related objects

For this project, the admin helps you inspect:

- users
- teams
- team memberships
- projects
- tasks

This is useful before building APIs because you can test whether the data model works correctly.

## Why Admin Is Useful in This Project

The project has several relationships:

- teams have memberships
- users join teams through memberships
- teams own projects
- projects contain tasks
- tasks are assigned to team memberships

The admin makes these relationships easier to understand visually.

For example:

- while editing a team, you can see its memberships
- while editing a project, you can see its tasks
- while editing a task, you can select assigned members
- while viewing a list of tasks, you can filter by completion state or project

This helps you check if the model design feels practical.

## Basic Admin Registration

The simplest way to show a model in Django admin is:

```python
from django.contrib import admin
from .models import Team

admin.site.register(Team)
```

This tells Django:

> Show this model in the admin panel.

But basic registration gives you a very plain admin page.

To customize how the model appears, use `ModelAdmin`.

## ModelAdmin

`ModelAdmin` lets you customize how a model behaves in the Django admin.

Example:

```python
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)
```

This gives the `Team` model a better admin interface.

Instead of only showing the default object name, you can control what appears in the list, how search works, and how records are ordered.

## Common Admin Options

### `list_display`

`list_display` controls which fields appear in the admin list page.

Example:

```python
list_display = ("name", "created_at", "updated_at")
```

This means the admin table will show:

- name
- created at
- updated at

Use `list_display` for fields you want to quickly see without opening each object.

Good example:

```python
list_display = ("title", "project", "is_done", "start_date", "end_date")
```

This is useful for tasks because you can quickly see the task title, project, status, and dates.

### `list_filter`

`list_filter` adds filters to the right side of the admin list page.

Example:

```python
list_filter = ("is_done", "project")
```

This lets you filter tasks by:

- done or not done
- project

Use `list_filter` for fields that have repeated values or categories.

Good fields for filters:

- choice fields
- boolean fields
- foreign keys
- dates

Examples:

```python
list_filter = ("role",)
list_filter = ("status",)
list_filter = ("is_done",)
list_filter = ("created_at",)
```

### `search_fields`

`search_fields` adds a search box to the admin list page.

Example:

```python
search_fields = ("title", "description")
```

This lets you search tasks by title or description.

You can also search through related models using double underscores.

Example:

```python
search_fields = ("title", "project__name")
```

This means:

> Search task title and the related project's name.

Useful examples:

```python
search_fields = ("name",)
search_fields = ("email", "first_name", "last_name")
search_fields = ("team__name", "user__email")
```

### `ordering`

`ordering` controls the default order of records in the admin list page.

Example:

```python
ordering = ("name",)
```

This orders records alphabetically by name.

Descending order uses `-`.

Example:

```python
ordering = ("-created_at",)
```

This shows the newest records first.

Use ordering to make the admin easier to browse.

### `readonly_fields`

`readonly_fields` makes some fields visible but not editable.

Example:

```python
readonly_fields = ("created_at", "updated_at")
```

This is useful for fields that Django manages automatically.

For example, `created_at` and `updated_at` should usually not be edited manually.

They are useful to see, but they should stay read-only.

### `autocomplete_fields`

`autocomplete_fields` makes foreign key or many-to-many selection easier.

Example:

```python
autocomplete_fields = ("team",)
```

Instead of showing a huge dropdown of all teams, Django shows a searchable input.

This is useful when the related table may grow.

Examples:

```python
autocomplete_fields = ("team",)
autocomplete_fields = ("project",)
autocomplete_fields = ("assigned_members",)
autocomplete_fields = ("user",)
```

Important: the related model admin usually needs `search_fields` for autocomplete to work well.

For example, if `TaskAdmin` has:

```python
autocomplete_fields = ("project",)
```

Then `ProjectAdmin` should have something like:

```python
search_fields = ("name",)
```

So Django knows how to search projects.

## Inline Admin Models

Inline admin lets you edit related child objects inside the parent object's admin page.

Example:

```python
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
```

Then inside `ProjectAdmin`:

```python
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
```

This means:

> When editing a project, show its tasks on the same page.

## When to Use Inline Admin

Use an inline when the relationship is parent to children.

Good examples in this project:

- Team to TeamMembership
- Project to Task

This makes sense because:

- a team has many memberships
- a project has many tasks

So while editing a team, it is useful to see or edit memberships.

While editing a project, it is useful to see or edit tasks.

## When Not to Use Inline Admin

Do not use an inline just because two models are related.

Example:

- Project to Team

A project belongs to one team, but the team is not a child of the project.

So you should not inline `Team` inside `ProjectAdmin`.

Instead, use a normal foreign key field or `autocomplete_fields`.

Good rule:

> Use inline admin when editing a parent and you want to manage its children.

## `TabularInline`

`TabularInline` shows related objects in a compact table format.

Example:

```python
class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
```

This is useful when child objects have only a few important fields.

For example, memberships can be shown as rows inside the team page.

## `StackedInline`

`StackedInline` shows related objects in a larger block layout.

It takes more space than `TabularInline`.

Use it when the child model has many fields or needs more room.

For this project, `TabularInline` is usually enough.

## `extra`

`extra` controls how many empty inline forms Django shows.

Example:

```python
extra = 1
```

This means Django shows one empty row for adding a new related object.

If you do not want extra empty rows, you can use:

```python
extra = 0
```

## Admin for Team and TeamMembership

The team admin is useful because a team has memberships.

A good setup may include:

```python
class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    autocomplete_fields = ("user",)
```

This allows memberships to be managed while editing a team.

The separate `TeamMembershipAdmin` is also useful because sometimes you want to search memberships directly.

For example:

```python
search_fields = ("team__name", "user__email")
list_filter = ("role",)
autocomplete_fields = ("team", "user")
```

This allows you to find memberships by team, user, or role.

## Admin for Project and Task

The project admin is useful because a project has tasks.

A good setup may include a `TaskInline`.

This allows tasks to be viewed or added while editing a project.

The task admin is also useful on its own because tasks are often searched and filtered directly.

For example:

```python
list_display = ("title", "project", "is_done", "start_date", "end_date")
list_filter = ("is_done", "project")
search_fields = ("title", "description", "project__name")
autocomplete_fields = ("project", "assigned_members")
```

This makes tasks easier to browse and manage.

## Admin Is Not Business Logic

Django admin should help with data management, but it should not become the main place for business logic.

For example, the admin can help you assign a task to a team member.

But the deeper business rule is:

> A task should only be assigned to members of the same team as the project.

That rule should later be handled more carefully using validation, serializers, or services.

Admin is useful for development and internal management, but the project still needs proper validation and permissions later.

## What This Phase Teaches

This phase teaches how to make models easier to inspect and manage.

Important ideas:

- register models in admin
- customize list pages
- add search
- add filters
- order records
- use autocomplete for related objects
- use inline admin for parent-child relationships
- avoid putting too much logic in admin

## Summary

Django admin is a powerful built-in tool for managing project data.

In this phase, admin was added so the data model can be inspected before building APIs.

The most important lesson is:

> Admin helps you understand and manage your models, but it is not a replacement for the real application interface.

After this phase, the project has:

- core models
- model relationships
- admin pages
- searchable and filterable records
- inline editing for useful parent-child relationships

This makes the project easier to test and understand before moving to ORM practice and APIs.
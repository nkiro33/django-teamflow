# Phase 2 — Django Admin Setup

In Phase 1, the core data model was created.

The project is built around a simple team-based project management system:

- users can belong to teams
- teams have memberships
- teams own projects
- projects contain tasks
- tasks can be assigned to team members

The main goal of Phase 1 was to design the database structure and understand how the models relate to each other.

## What This Phase Adds

In this phase, Django admin configuration was added for the project models.

The admin is not the final user interface for this project. It is a developer tool that helps you inspect, create, update, and manage data while building the backend.

This phase makes it easier to see whether the model relationships are working correctly before building APIs.

## Admin Areas Added

Admin setup was added for the main apps:

- `users`
- `teams`
- `projects`

The admin now supports managing:

- users
- teams
- team memberships
- projects
- tasks

## Why Django Admin Matters

Django admin is useful because it gives you a quick way to work with your data without building custom views or API endpoints first.

It helps you:

- inspect model records
- create sample data manually
- test relationships between models
- search and filter records
- manage related objects from one place
- check whether your model design feels practical

For example:

- a team can show its memberships
- a project can show its tasks
- foreign key fields can use autocomplete
- list pages can show the most useful fields
- filters make large sets of data easier to browse

## What You Should Learn From This Phase

This phase introduces practical admin concepts such as:

- `ModelAdmin`
- `list_display`
- `list_filter`
- `search_fields`
- `ordering`
- `readonly_fields`
- `autocomplete_fields`
- inline admin models

The main idea is that admin should make development and inspection easier.

It should not be treated as the final product interface.

## What Is Still Not Included

This phase does not include:

- APIs
- serializers
- authentication flows
- permissions
- service layer logic
- billing logic
- background tasks

Those topics will come later.

## Current Project State

At this point, the project has:

- core models
- model relationships
- Django admin setup
- a better way to inspect and manage data

This gives the project a stronger foundation before moving into ORM practice and API development.
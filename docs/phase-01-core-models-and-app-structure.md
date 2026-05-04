# Phase 1 — Core Models and App Structure

This phase introduces the foundation of the Django TeamFlow project.

The goal is to understand how a Django backend project should be organized before adding APIs, authentication, permissions, billing, or background tasks.

This phase focuses on core modeling and project structure.

## Phase Goal

By the end of this phase, the learner should understand:

- what a Django app is
- why projects are split into apps
- how models represent business concepts
- how model relationships work
- when to use `ForeignKey`
- when to use `ManyToManyField`
- why a through model is useful
- how to think about app boundaries

This phase is intentionally focused.

It does not try to teach everything at once.

## Main Project Idea

The project is a team-based project management backend.

The core domain is:

- Teams
- Team Memberships
- Projects
- Tasks

A simple version of the system looks like this:

- A team has members.
- A team owns projects.
- A project has tasks.
- A task can be assigned to team members.

This gives us enough structure to learn real Django modeling without making the project too complex too early.

## Why Start with Models?

Models are one of the most important parts of a Django project.

A model is not just a database table.

A model represents an important concept in the system.

Examples from this project:

- `Team`
- `TeamMembership`
- `Project`
- `Task`

Each model should answer a clear question.

Examples:

- `Team`: What group owns this work?
- `Project`: What work belongs to this team?
- `Task`: What needs to be done inside this project?
- `TeamMembership`: Which user belongs to which team, and with what role?

Good models make the rest of the project easier.

Bad models make views, APIs, permissions, and business logic harder later.

## Why Use Multiple Django Apps?

A Django project can contain many apps.

An app is a focused section of the project.

In this project, we use separate apps because each part of the system has a different responsibility.

Current apps:

- `teams`
- `projects`
- `users`
- `core`

For this phase, the main focus is on:

- `teams`
- `projects`

The `users` app exists, but it is not the main beginner topic yet.

## App Responsibility

A good app should own one clear part of the domain.

Example responsibilities:

- `teams` app → team and membership concepts
- `projects` app → project and task concepts
- `users` app → account and identity concepts
- `core` app → shared project-level utilities

This separation helps the project stay maintainable.

As a project grows, unclear app boundaries can cause code to become messy.

## Good App Boundary Rule

A useful rule is:

> Put code close to the business concept it belongs to.

Examples:

- `TeamMembership` belongs in `teams`.
- `Project` belongs in `projects`.
- `Task` belongs in `projects`.
- User account logic belongs in `users`.
- Billing plan logic should later belong in `billing`.

Avoid putting everything into one large app.

Also avoid using `core` as a dumping ground.

The `core` app should stay small and only contain shared project-level utilities.

## Why Users Are Skipped for Now

The project may include a custom user model, but this phase does not explain it deeply.

Custom user models are important, but they are not beginner-friendly as a first topic.

They involve several Django auth concepts:

- `AbstractUser`
- `BaseUserManager`
- `USERNAME_FIELD`
- `REQUIRED_FIELDS`
- `AUTH_USER_MODEL`
- email login
- superuser creation
- authentication behavior

Those are useful later, but they can distract from the first goal: understanding app structure and model relationships.

For now, learners only need to understand this:

> A user can belong to teams through `TeamMembership`.

The deeper details of custom users, login, and permissions will come in a later phase.

## The Teams App

The `teams` app owns the team-related part of the system.

It contains:

- `Team`
- `TeamMembership`

## Team Model

The `Team` model represents a workspace or group.

Examples:

- Engineering Team
- Design Team
- Marketing Team

A team can have many users.

A team can also have many projects.

Important fields:

- `name`
- `description`
- `created_at`
- `updated_at`

The team model should stay focused on team-level information.

It should not store task data, project details, billing logic, or user profile data directly.

## TeamMembership Model

The `TeamMembership` model connects a user to a team.

This is one of the most important models in the project.

A simple many-to-many relationship between teams and users would only tell us:

> This user belongs to this team.

But our system needs more information.

It also needs to know:

> What role does this user have in this team?

That is why we use a separate model.

## Why TeamMembership Is Better Than a Simple ManyToMany

A normal many-to-many relationship is good when the relationship has no extra data.

Example:

- `Article` ↔ `Tag`

The relationship only means:

> This article has this tag.

But team membership has extra meaning.

It includes a role:

- `owner`
- `admin`
- `member`

So we need a through model.

Conceptually:

> User joins Team through TeamMembership.

This gives us a place to store relationship-specific data.

## Why Role Belongs on TeamMembership

A common beginner mistake is to put role directly on the user.

Example of the wrong idea:

`User.role = "admin"`

That works only if the user has one role in the whole system.

But this project is team-based.

One user can belong to many teams.

The same user may have different roles in different teams.

Example:

- Mariam is owner of Team A.
- Mariam is member of Team B.
- Mariam is admin of Team C.

So role cannot belong globally to the user.

The role belongs to the relationship between the user and the team.

That relationship is `TeamMembership`.

## Unique Membership Rule

The project should not allow the same user to be added to the same team twice.

This is a business rule.

Conceptually:

> One user can have only one membership per team.

But the same user can still belong to many different teams.

And the same team can still have many different users.

This is why the model uses a uniqueness rule for:

- `team`
- `user`

This teaches an important idea:

> Some business rules can be represented directly in the database model.

## The Projects App

The `projects` app owns project-related work.

It contains:

- `Project`
- `Task`

## Project Model

The `Project` model represents work owned by a team.

Examples:

- Website Redesign
- New Mobile App
- Internal Dashboard

A project belongs to one team.

A team can have many projects.

This is a classic one-to-many relationship.

In Django, this is modeled with `ForeignKey`.

Conceptually:

> Project → Team

This means:

- Each project has one team.
- Each team can have many projects.

Important fields:

- `team`
- `name`
- `description`
- `start_date`
- `end_date`
- `created_at`
- `updated_at`

## Why Project Has a ForeignKey to Team

Use `ForeignKey` when many records belong to one parent.

In this case:

> Many projects can belong to one team.

So the child model stores the `ForeignKey`.

That means `Project` stores a reference to `Team`.

The relationship is:

- Team has many Projects.
- Project belongs to one Team.

## Optional End Date

The project has `end_date` as an optional field.

This is realistic because some projects may start before the final end date is known.

So the field allows:

- `blank=True`
- `null=True`

Conceptually:

- `blank=True` → form/admin/API input can leave it empty
- `null=True` → database can store `NULL`

This distinction is important in Django.

## Task Model

The `Task` model represents a unit of work inside a project.

Examples:

- Create landing page
- Design pricing section
- Fix login bug
- Write API documentation

A task belongs to one project.

A project can have many tasks.

This is another one-to-many relationship.

Conceptually:

> Task → Project

Important fields:

- `project`
- `assigned_members`
- `title`
- `description`
- `start_date`
- `end_date`
- `is_done`
- `created_at`
- `updated_at`

## Why Task Has a ForeignKey to Project

A task should not exist by itself in this system.

It belongs inside a project.

So `Task` has a `ForeignKey` to `Project`.

This means:

- Each task belongs to one project.
- Each project can have many tasks.

This keeps the work organized.

## Why Task Assignment Uses ManyToMany

A task may be assigned to more than one person.

Example:

> One task may need both a designer and a backend developer.

So a task needs multiple assigned members.

This is why assignment uses `ManyToManyField`.

Conceptually:

> Task ↔ TeamMembership

This means:

- One task can have many assigned members.
- One team member can have many tasks.

## Why Tasks Are Assigned to TeamMembership, Not User

This is an important design choice.

A beginner might assign a task directly to a user.

Example:

> Task → User

But this project is team-based.

A task belongs to a project.

A project belongs to a team.

So the person assigned to the task should be a member of that team.

That means the better relationship is:

> Task → TeamMembership

This says:

> This task is assigned to this user as a member of this team.

That is more accurate than saying:

> This task is assigned to this global user account.

This design will help later when adding permissions and business rules.

## Important Business Rule Not Fully Enforced Yet

There is an important rule:

> A task should only be assigned to members of the same team that owns the project.

Example:

> If Project A belongs to Team A, then Task A should only be assigned to memberships from Team A.

This rule is important, but it is not fully enforced yet.

That is okay for this phase.

Later, it can be enforced using:

- serializer validation
- service layer logic
- model validation
- database constraints where possible

This teaches another important idea:

> Not every business rule must be solved in the first model version.

Start with a clear model.

Then add validation when the project reaches the right phase.

## Relationship Summary

The main relationships are:

- `Team`
  - has many `TeamMembership` records
  - has many `Project` records
  - has many `User` records through `TeamMembership`

- `Project`
  - belongs to one `Team`

- `Task`
  - belongs to one `Project`
  - has many assigned `TeamMembership` records

- `TeamMembership`
  - belongs to one `Team`
  - belongs to one `User`

Task assignment:

> Task ↔ TeamMembership

## ForeignKey

A `ForeignKey` represents a many-to-one relationship.

Use it when many child records belong to one parent.

Examples in this project:

- `Project` → `Team`
- `Task` → `Project`
- `TeamMembership` → `Team`
- `TeamMembership` → `User`

Read these as:

- A project belongs to one team.
- A task belongs to one project.
- A membership belongs to one team.
- A membership belongs to one user.

## ManyToManyField

A `ManyToManyField` represents a many-to-many relationship.

Use it when many records on one side can connect to many records on the other side.

Examples:

- `Team` ↔ `User`
- `Task` ↔ `TeamMembership`

In this project, `Team` and `User` are connected through `TeamMembership`.

This is because the relationship needs extra data, such as role.

## Through Model

A through model is used when a many-to-many relationship needs extra fields.

In this project, `TeamMembership` is the through model between:

- `Team`
- `User`

It stores:

- `team`
- `user`
- `role`
- `created_at`
- `updated_at`

Without a through model, there would be no clean place to store the user's role inside the team.

## related_name

`related_name` controls how you access related objects from the other side of a relationship.

Example ideas:

- `team.projects.all()`
- `project.tasks.all()`
- `team.memberships.all()`

Good `related_name` values make code easier to read.

They should describe the relationship clearly.

Avoid confusing or overly generic names.

## Timestamps

Many models use:

- `created_at`
- `updated_at`

These fields are useful in almost every backend project.

They help answer questions like:

- When was this created?
- When was this last changed?

Common Django options:

- `auto_now_add=True`
- `auto_now=True`

Meaning:

- `auto_now_add=True` → set once when the row is created
- `auto_now=True` → update every time the row is saved

## Model `__str__` Method

The `__str__` method controls how a model object appears as text.

This is useful in:

- Django admin
- Django shell
- debugging
- logs
- printed query results

A clear `__str__` method makes development easier.

## What This Phase Should Teach

This phase should teach more than just syntax.

The main lesson is how to think about data modeling.

Important questions:

- What is the main object?
- Who owns this object?
- Can this object exist by itself?
- Is this a one-to-many relationship?
- Is this a many-to-many relationship?
- Does the relationship need extra data?
- Where should this business rule live?

These questions matter more than memorizing field types.

## What This Phase Should Not Teach Yet

This phase should not go deep into:

- admin customization
- REST APIs
- serializers
- authentication
- permissions
- billing
- services
- background tasks
- deployment
- testing

Those are important, but they should come later.

Trying to teach them now would make the project harder for beginners to follow.

## Brief Preview of Future Layers

Although this phase focuses on models, learners should know what comes later.

## Views

Views handle requests and return responses.

Later, views will be used to expose project data through web pages or APIs.

For now, learners only need to know:

> Views are not the place to design the database model.

Models come first.

## URLs

URLs connect request paths to views.

Example:

> `/projects/` could later point to a view that lists projects.

For now, URLs are not the main focus.

## Serializers

Serializers are usually introduced with Django REST Framework.

They help with:

- converting model objects into API responses
- validating incoming request data
- creating and updating model instances from API input

Serializers will become important when APIs are added.

## Service Layer

A service layer is a place for business workflows.

Examples:

- create a project
- assign a task to a team member
- invite a user to a team
- check whether a team reached its plan limit

Services are not needed deeply in this first phase.

They become more useful when the project has more business rules.

## Billing Is Not Part of This Phase

Billing may exist later, but it should not be part of the beginner model explanation.

Billing introduces more advanced ideas:

- subscription plans
- team limits
- billing status
- payment state
- business validation
- service-layer checks

For this project, billing should initially be used to teach what a team is allowed to use, not real payment processing.

Payment providers, invoices, and webhooks should come much later, if needed.

## Good Beginner Mental Model

For this phase, learners can think of the project like this:

- A team owns work.
- A project belongs to a team.
- A task belongs to a project.
- A user joins a team through membership.
- A task is assigned to a team member.

That is the core idea.

## Summary

Phase 1 creates the foundation of the project.

The most important ideas are:

- Use apps to separate responsibilities.
- Use models to represent business concepts.
- Use `ForeignKey` for many-to-one relationships.
- Use `ManyToManyField` for many-to-many relationships.
- Use a through model when the relationship has extra data.
- Put team role on `TeamMembership`, not `User`.
- Assign tasks to `TeamMembership`, not directly to `User`.
- Keep custom users, auth, permissions, billing, and APIs for later phases.

A strong Django project starts with clear data modeling.

This phase is about building that foundation.
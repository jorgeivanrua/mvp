# Requirements Document - Sistema de Personalización de Fondos

## Introduction

El Sistema de Personalización de Fondos permite al Super Admin personalizar la apariencia de la página de login del sistema electoral mediante la gestión de fondos visuales. El sistema soporta tres tipos de fondos: gradientes de colores, imágenes personalizadas y colores sólidos. Incluye fondos predefinidos para selección rápida y permite la subida de imágenes personalizadas con preview en tiempo real.

## Glossary

- **Sistema**: Sistema Electoral de Recolección de Datos
- **Super Admin**: Usuario con rol de administrador supremo del sistema
- **Fondo**: Configuración visual aplicada al fondo de la página de login
- **Gradiente**: Transición suave entre dos o más colores
- **Overlay**: Capa semitransparente aplicada sobre un fondo
- **Preview**: Vista previa en tiempo real de cómo se verá el fondo
- **Fondo Activo**: Fondo actualmente aplicado a la página de login
- **Fondo Predefinido**: Fondo preconfigurado disponible para selección rápida

## Requirements

### Requirement 1: Gestión de Fondos de Login

**User Story:** As a Super Admin, I want to manage login background configurations, so that I can customize the visual appearance of the login page.

#### Acceptance Criteria

1. WHEN the Super Admin accesses the background management interface THEN the System SHALL display all available backgrounds in a grid layout
2. WHEN displaying backgrounds THEN the System SHALL show the background name, type, preview, active status, and creation date
3. WHEN a background is marked as active THEN the System SHALL apply it to the login page immediately
4. WHEN the Super Admin creates a new background THEN the System SHALL validate the configuration and save it to the database
5. WHEN the Super Admin deletes a background THEN the System SHALL remove it from the database and delete associated files if applicable

### Requirement 2: Tipos de Fondos - Gradientes

**User Story:** As a Super Admin, I want to create gradient backgrounds, so that I can use smooth color transitions as login backgrounds.

#### Acceptance Criteria

1. WHEN creating a gradient background THEN the System SHALL accept up to three colors in hexadecimal format
2. WHEN configuring a gradient THEN the System SHALL allow selection of gradient direction (0deg, 45deg, 90deg, 135deg, 180deg)
3. WHEN a gradient has three colors THEN the System SHALL distribute them as: color1 (0-50%), color2 (50-75%), color3 (75-100%)
4. WHEN a gradient has two colors THEN the System SHALL create a smooth transition from color1 to color2
5. WHEN displaying a gradient preview THEN the System SHALL render the gradient using CSS linear-gradient

### Requirement 3: Tipos de Fondos - Imágenes

**User Story:** As a Super Admin, I want to upload custom images as backgrounds, so that I can use photographs or graphics on the login page.

#### Acceptance Criteria

1. WHEN uploading an image THEN the System SHALL accept only png, jpg, jpeg, gif, and webp formats
2. WHEN an image is uploaded THEN the System SHALL generate a unique filename using UUID to prevent conflicts
3. WHEN configuring an image background THEN the System SHALL allow selection of image position (center, top, bottom, left, right)
4. WHEN configuring an image background THEN the System SHALL allow selection of image size (cover, contain, auto)
5. WHEN an image background is deleted THEN the System SHALL remove the image file from the server filesystem

### Requirement 4: Tipos de Fondos - Colores Sólidos

**User Story:** As a Super Admin, I want to create solid color backgrounds, so that I can use simple, clean colors on the login page.

#### Acceptance Criteria

1. WHEN creating a solid color background THEN the System SHALL accept a color in hexadecimal format
2. WHEN displaying a solid color background THEN the System SHALL apply the color uniformly across the entire login page
3. WHEN previewing a solid color THEN the System SHALL show the exact color that will be applied

### Requirement 5: Fondos Predefinidos

**User Story:** As a Super Admin, I want to select from predefined backgrounds, so that I can quickly apply professional-looking backgrounds without custom configuration.

#### Acceptance Criteria

1. WHEN accessing predefined backgrounds THEN the System SHALL provide at least 7 predefined options
2. WHEN displaying predefined backgrounds THEN the System SHALL include: Bandera de Colombia, Azul Institucional, Amarillo Vibrante, Rojo Patriótico, Azul Oscuro, Gradiente Amanecer, and Gradiente Océano
3. WHEN a predefined background is selected THEN the System SHALL create a new background record with the predefined configuration
4. WHEN displaying predefined backgrounds THEN the System SHALL show a visual preview of each option
5. WHEN the Bandera de Colombia background is used THEN the System SHALL display a three-color gradient with yellow (0-50%), blue (50-75%), and red (75-100%)

### Requirement 6: Preview en Tiempo Real

**User Story:** As a Super Admin, I want to see a real-time preview of backgrounds, so that I can visualize how they will look before activating them.

#### Acceptance Criteria

1. WHEN creating or editing a background THEN the System SHALL display a live preview panel
2. WHEN changing background colors THEN the System SHALL update the preview immediately without page reload
3. WHEN adjusting gradient direction THEN the System SHALL reflect the change in the preview instantly
4. WHEN uploading an image THEN the System SHALL show the image in the preview before saving
5. WHEN configuring overlay settings THEN the System SHALL apply the overlay to the preview in real-time

### Requirement 7: Activación de Fondos

**User Story:** As a Super Admin, I want to activate a background, so that it becomes the current background for the login page.

#### Acceptance Criteria

1. WHEN activating a background THEN the System SHALL deactivate all other backgrounds automatically
2. WHEN a background is activated THEN the System SHALL mark it with activo=True in the database
3. WHEN no background is active THEN the System SHALL use the default Bandera de Colombia gradient
4. WHEN the login page loads THEN the System SHALL query the active background and apply it
5. WHEN a background is activated THEN the System SHALL apply the change immediately for all users

### Requirement 8: Eliminación de Fondos

**User Story:** As a Super Admin, I want to delete backgrounds, so that I can remove unused or unwanted background configurations.

#### Acceptance Criteria

1. WHEN deleting a background THEN the System SHALL verify it is not currently active
2. WHEN attempting to delete an active background THEN the System SHALL reject the operation with an error message
3. WHEN deleting an image background THEN the System SHALL remove the associated image file from the filesystem
4. WHEN a background is deleted THEN the System SHALL remove it from the database permanently
5. WHEN deletion fails THEN the System SHALL rollback the database transaction and preserve the background

### Requirement 9: Overlay Opcional

**User Story:** As a Super Admin, I want to add a semi-transparent overlay to backgrounds, so that I can improve text readability on the login page.

#### Acceptance Criteria

1. WHEN configuring a background THEN the System SHALL allow adding an optional overlay color
2. WHEN an overlay is configured THEN the System SHALL accept an opacity value between 0.0 and 1.0
3. WHEN an overlay is applied THEN the System SHALL render it as a semi-transparent layer over the background
4. WHEN no overlay is configured THEN the System SHALL display the background without any overlay layer
5. WHEN previewing a background with overlay THEN the System SHALL show the overlay effect in the preview

### Requirement 10: Permisos y Seguridad

**User Story:** As a system administrator, I want background management restricted to Super Admins only, so that unauthorized users cannot modify the login page appearance.

#### Acceptance Criteria

1. WHEN a non-Super Admin user attempts to access background management THEN the System SHALL return a 403 Forbidden error
2. WHEN creating a background THEN the System SHALL record the user ID of the Super Admin who created it
3. WHEN uploading an image THEN the System SHALL validate the file type to prevent malicious uploads
4. WHEN saving a background THEN the System SHALL sanitize all input data to prevent injection attacks
5. WHEN the login page loads the active background THEN the System SHALL use a public endpoint that does not require authentication

### Requirement 11: Carga Dinámica en Login

**User Story:** As a system user, I want the login page to load with the active background automatically, so that I see the customized appearance without additional configuration.

#### Acceptance Criteria

1. WHEN the login page loads THEN the System SHALL query the active background from the database
2. WHEN no active background exists THEN the System SHALL apply the default Bandera de Colombia gradient
3. WHEN the active background is a gradient THEN the System SHALL generate the appropriate CSS linear-gradient
4. WHEN the active background is an image THEN the System SHALL load the image with configured position and size
5. WHEN the active background is a solid color THEN the System SHALL apply the color to the page background

### Requirement 12: Almacenamiento de Archivos

**User Story:** As a system administrator, I want uploaded images stored securely, so that they are accessible to the login page but protected from unauthorized access.

#### Acceptance Criteria

1. WHEN an image is uploaded THEN the System SHALL store it in the frontend/static/uploads/fondos directory
2. WHEN generating a filename THEN the System SHALL use UUID to ensure uniqueness and prevent overwrites
3. WHEN storing an image THEN the System SHALL preserve the original file extension
4. WHEN an image background is deleted THEN the System SHALL attempt to remove the file from the filesystem
5. WHEN the upload directory does not exist THEN the System SHALL create it automatically


/*
  Warnings:

  - You are about to drop the column `Collection` on the `patterns` table. All the data in the column will be lost.
  - Added the required column `collection` to the `patterns` table without a default value. This is not possible if the table is not empty.
  - Added the required column `discription` to the `patterns` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "patterns" DROP COLUMN "Collection",
ADD COLUMN     "collection" TEXT NOT NULL,
ADD COLUMN     "discription" TEXT NOT NULL;

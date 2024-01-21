import { Injectable } from '@nestjs/common';
import { Prisma} from '@prisma/client';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class UsersService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createUserDto: Prisma.usersCreateInput) {
    return this.databaseService.users.create({
      data: createUserDto
    });
  }

  async findAll() {
    return this.databaseService.users.findMany;
  }

  async findOne(email: string) {
    return this.databaseService.users.findUnique({
      where:{
        email,
      },
    });
  }

  async update(email: string, updateUserDto: Prisma.usersUpdateInput) {
    return this.databaseService.users.update({
      where:{
        email,
      },
      data: updateUserDto
    });
  }

  async remove(email: string) {
    return this.databaseService.users.delete({
      where:{
        email,
      }
    });
  }
}



